# main.py — Robust stripe-phase estimator + AUTO_TRIM (USB + optional BLE)
# - Robust TEST: nearest-neighbor edge pairing + modulo wrapping + median
# - AUTO_TRIM: small safe steps until |phase| < 15 ms
# - NUDGE_TRIM kept (locale-tolerant), now safer; SET_TRIM syncs fwd/rev
# - Optional sensor↔motor mapping self-check

from machine import Pin, PWM, ADC
import utime, ujson, sys

# ========= PINOUT =========
LEFT_SERVO_PIN  = 14
RIGHT_SERVO_PIN = 13
LEFT_IR_PIN     = 32
RIGHT_IR_PIN    = 33
BUZZER_PIN      = 25

# ========= SERVO =========
SERVO_FREQ_HZ = 50
US_MIN=1000; US_STOP=1500; US_MAX=2000
US_STOP_L = US_STOP
US_STOP_R = US_STOP

# ========= FORWARD MAPPING (±1) =========
# If "Jog +" doesn't move forward, click "Flip Forward" in UI (SET_DIR -1 +1 or via your page).
DIR_L_DEFAULT = +1
DIR_R_DEFAULT = -1

# ========= PARAMS =========
BASE_SPEED        = 40
MAX_TRIM          = 0.40
SAMPLE_MS         = 5
EDGE_DEB_MS       = 25
HYST              = 0.10
COUNTDOWN_SEC     = 5

# Safe limits for trim stepping
NUDGE_GAIN_DEFAULT = 0.5         # smaller = gentler
NUDGE_STEP_MAX     = 0.06        # abs trim change per nudge
AUTO_STEP_MAX      = 0.06        # abs trim change per auto-iteration
AUTO_GAIN          = 0.6         # auto-trim proportional gain
AUTO_THRESH_MS     = 15.0        # stop when |phase| < this
AUTO_ITERS_DEF     = 8

CAL_FILE = "calibration.json"

def _clamp(x,a,b):
    if x<a: return a
    if x>b: return b
    return x

def _coerce_float(s):
    # Locale-tolerant numeric parse (commas, unicode minus)
    s = str(s).strip()
    try:
        s = s.replace(',', '.')
        s = s.replace('\u2212','-').replace('\u2012','-').replace('\u2013','-').replace('\u2014','-')
    except:
        pass
    out=[]
    for ch in s:
        if ch in '0123456789.+-eE': out.append(ch)
    s=''.join(out)
    if not s or s in ('+','-','.','+.','-.'): raise ValueError('invalid number')
    return float(s)

# ===== Buzzer (optional) =====
class Buzzer:
    def __init__(self, pin=BUZZER_PIN):
        self.pin_id = pin
        self.pwm = None
        self.ok = True
    def _ensure(self):
        if self.pwm is None:
            try:
                self.pwm = PWM(Pin(self.pin_id))
                try: self.pwm.freq(2000)
                except: pass
                try: self.pwm.duty_u16(0)
                except:
                    try: self.pwm.duty(0)
                    except: self.ok=False
            except:
                self.ok=False
    def _duty01(self, v):
        try:
            if hasattr(self.pwm, "duty_u16"): self.pwm.duty_u16(int(65535*_clamp(v,0,1)))
            else: self.pwm.duty(int(1023*_clamp(v,0,1)))
        except: pass
    def beep_ms(self, ms=120, freq=2000, duty=0.4):
        if not self.ok: utime.sleep_ms(ms); return
        self._ensure()
        if not self.ok: utime.sleep_ms(ms); return
        try: self.pwm.freq(freq)
        except: pass
        self._duty01(duty); utime.sleep_ms(ms); self._duty01(0)
        try: self.pwm.deinit(); self.pwm=None
        except: pass
    def countdown(self, sec=5):
        for i in range(sec, 0, -1):
            self.beep_ms(120, 1800 + 60*i, 0.45 if i==1 else 0.32)
            utime.sleep_ms(880)

# ===== Servo 360 =====
class Servo360:
    def __init__(self, pin, us_stop):
        self.pwm = PWM(Pin(pin), freq=SERVO_FREQ_HZ)
        self.us_stop = us_stop
        self.period_us = int(1000000 // SERVO_FREQ_HZ)
        self.set_speed(0)
    def _us_to_duty(self, us): return int(us * 65535 // self.period_us)
    def set_us(self, us): self.pwm.duty_u16(self._us_to_duty(int(us)))
    def set_speed(self, spd):
        span=(US_MAX-US_MIN)/2.0
        self.set_us(self.us_stop + span*(_clamp(spd,-100,100)/100.0))

# ===== Analog IR =====
class AnalogIR:
    def __init__(self, pin):
        self.adc = ADC(Pin(pin))
        try: self.adc.atten(ADC.ATTN_11DB)
        except: pass
        self.filt=0.5; self.alpha=0.25
        self.minv=1.0; self.maxv=0.0
        self.th_lo=0.4; self.th_hi=0.6
        self.state=0; self._last_ms=0
        self._learn_on=False
        self.fixed=True
    def _read_norm(self):
        v=self.adc.read_u16()/65535.0
        self.filt += self.alpha*(v-self.filt)
        return self.filt
    def read(self, now_ms):
        v=self._read_norm()
        st=self.state; edge=0
        if st==0 and v>=self.th_hi and (now_ms-self._last_ms)>=EDGE_DEB_MS:
            st=1; edge=+1; self._last_ms=now_ms
        elif st==1 and v<=self.th_lo and (now_ms-self._last_ms)>=EDGE_DEB_MS:
            st=0; edge=-1; self._last_ms=now_ms
        self.state=st
        return st, edge

# ===== Robot =====
class Otto:
    def __init__(self):
        self.left  = Servo360(LEFT_SERVO_PIN,  US_STOP_L)
        self.right = Servo360(RIGHT_SERVO_PIN, US_STOP_R)
        self.irL = AnalogIR(LEFT_IR_PIN)
        self.irR = AnalogIR(RIGHT_IR_PIN)
        self.buz = Buzzer(BUZZER_PIN)
        self.dir_l = DIR_L_DEFAULT
        self.dir_r = DIR_R_DEFAULT
        self.trim_fwd = 0.0
        self.trim_rev = 0.0
        self.motor_enable = True
        self._quality = None
        self._last_phase_ms = None
        self._last_period_ms = None
        self._mapping_checked = False
        self._load()

    # ---- storage ----
    def _load(self):
        try:
            with open("calibration.json","r") as f:
                d=ujson.load(f)
            self.dir_l=int(d.get("dir_l", DIR_L_DEFAULT))
            self.dir_r=int(d.get("dir_r", DIR_R_DEFAULT))
            if self.dir_l not in(-1,1): self.dir_l=DIR_L_DEFAULT
            if self.dir_r not in(-1,1): self.dir_r=DIR_R_DEFAULT
            self.trim_fwd=float(d.get("trim_fwd", d.get("trim",0.0)))
            self.trim_rev=float(d.get("trim_rev", self.trim_fwd))
        except:
            pass
    def _save(self):
        try:
            data={"dir_l":self.dir_l,"dir_r":self.dir_r,
                  "trim_fwd":self.trim_fwd,"trim_rev":self.trim_rev}
            with open("calibration.json","w") as f:
                ujson.dump(data,f)
        except:
            pass

    # ---- motor io (robot frame) ----
    def _write_robot(self, l_cmd, r_cmd):
        if not self.motor_enable: return
        self.left.set_speed(self.dir_l*_clamp(l_cmd,-100,100))
        self.right.set_speed(self.dir_r*_clamp(r_cmd,-100,100))
    def stop(self): self._write_robot(0,0)

    # ---- optional: quick sensor↔motor mapping check (safe) ----
    def _check_and_fix_mapping(self, spd=30):
        if self._mapping_checked: return
        stL0=self.irL.state; stR0=self.irR.state
        Lm=[0,0]; Rm=[0,0]
        t0=utime.ticks_ms()
        while utime.ticks_diff(utime.ticks_ms(),t0) < 350:
            now=utime.ticks_ms(); self._write_robot(spd, 0)
            _,eL=self.irL.read(now); _,eR=self.irR.read(now)
            if eL: Lm[0]+=1
            if eR: Lm[1]+=1
            utime.sleep_ms(SAMPLE_MS)
        self.stop(); utime.sleep_ms(120)
        t1=utime.ticks_ms()
        while utime.ticks_diff(utime.ticks_ms(),t1) < 350:
            now=utime.ticks_ms(); self._write_robot(0, spd)
            _,eL=self.irL.read(now); _,eR=self.irR.read(now)
            if eL: Rm[0]+=1
            if eR: Rm[1]+=1
            utime.sleep_ms(SAMPLE_MS)
        self.stop()
        swap=False
        if Lm[1] > Lm[0]: swap=True
        if Rm[0] > Rm[1]: swap=True
        if swap:
            self.irL, self.irR = self.irR, self.irL
        self.irL.state=stL0; self.irR.state=stR0
        self._mapping_checked=True

    # ---- helpers: run with a FORCED trim (no saving), collect edge times ----
    def _run_collect_edges(self, T_force, spd, secs):
        self.irL.state=0; self.irR.state=0
        edgesL=[]; edgesR=[]
        t0=utime.ticks_ms()
        while utime.ticks_diff(utime.ticks_ms(),t0) < int(secs*1000):
            now=utime.ticks_ms()
            self._write_robot(spd*(1.0-T_force), spd*(1.0+T_force))
            _,eL=self.irL.read(now); _,eR=self.irR.read(now)
            if eL: edgesL.append(now)
            if eR: edgesR.append(now)
            utime.sleep_ms(SAMPLE_MS)
        self.stop()
        return edgesL, edgesR

    def _median(self, arr):
        n=len(arr)
        if n==0: return None
        arr2=sorted(arr)
        m=n//2
        if n%2==1: return arr2[m]
        return 0.5*(arr2[m-1]+arr2[m])

    def _robust_period(self, edges):
        if len(edges)<3: return None
        ds=[]
        for i in range(1,len(edges)):
            ds.append(utime.ticks_diff(edges[i], edges[i-1]))
        if not ds: return None
        p=self._median(ds)
        return p

    def _phase_from_edges(self, edgesL, edgesR):
        # robust: nearest-neighbor pairing + modulo wrap to (-0.5P, +0.5P), median
        if len(edgesL)<3 or len(edgesR)<3: return None, None, 0
        perL=self._robust_period(edgesL)
        perR=self._robust_period(edgesR)
        per=None
        if perL and perR: per=0.5*(perL+perR)
        elif perL: per=perL
        elif perR: per=perR
        if per is None or per<60: return None, None, 0

        # nearest neighbor, one-to-one-ish
        i=0; j=0; Nl=len(edgesL); Nr=len(edgesR)
        diffs=[]
        while i<Nl and j<Nr:
            tL=edgesL[i]; tR=edgesR[j]
            # move j to best neighbor for this tL
            while (j+1<Nr) and (abs(utime.ticks_diff(edgesR[j+1],tL)) < abs(utime.ticks_diff(edgesR[j],tL))):
                j+=1
            dt = utime.ticks_diff(tL, tR)  # signed ms
            # wrap into (-0.5P,+0.5P)
            k = int(round(dt/float(per)))
            dtw = dt - k*per
            if abs(dtw) <= 0.6*per:    # drop outliers
                diffs.append(dtw)
            i+=1; j+=1
        if len(diffs)<4: return None, per, len(diffs)
        phase = self._median(diffs)
        return phase, per, len(diffs)

    # ---- TEST (uses saved trim for forward) ----
    def test(self, spd, secs):
        self._check_and_fix_mapping()
        T = self.trim_fwd if spd>=0 else self.trim_rev
        eL,eR = self._run_collect_edges(T, spd, secs)
        phase, per, m = self._phase_from_edges(eL, eR)
        if phase is None:
            self._quality=None; self._last_phase_ms=None; self._last_period_ms=None
            return {"ok":False,"reason":"not enough matched edges","edgesL":len(eL),"edgesR":len(eR),"matches":m}
        self._last_phase_ms = phase
        self._last_period_ms = per
        self._quality = abs(phase)
        return {"ok": abs(phase)<AUTO_THRESH_MS,
                "avg_phase_ms": round(phase,1),
                "period_ms": round(per,1),
                "matches": m,
                "trim_used": round(T,4)}

    # ---- NUDGE_TRIM (safer) ----
    def nudge_trim(self, phase_ms, gain=NUDGE_GAIN_DEFAULT):
        per = self._last_period_ms
        if per is None or per <= 0:
            return {"ok":False,"reason":"no_period_measurement (run TEST first)"}
        norm = phase_ms / per
        # safe capped step
        delta = -gain * norm
        if delta >  NUDGE_STEP_MAX: delta =  NUDGE_STEP_MAX
        if delta < -NUDGE_STEP_MAX: delta = -NUDGE_STEP_MAX
        T_new = _clamp(self.trim_fwd + delta, -MAX_TRIM, MAX_TRIM)
        self.trim_fwd = T_new
        self.trim_rev = T_new
        self._save()
        return {"ok":True, "trim_fwd": round(self.trim_fwd,4),
                "delta": round(delta,4), "norm": round(norm,4),
                "used_period_ms": round(per,1)}

    # ---- AUTO_TRIM: small steps until straight ----
    def auto_trim(self, spd=40, secs=2.2, iters=AUTO_ITERS_DEF):
        self._check_and_fix_mapping()
        hist=[]
        for k in range(iters):
            # measure using current trim
            eL,eR = self._run_collect_edges(self.trim_fwd, spd, secs)
            phase, per, m = self._phase_from_edges(eL, eR)
            if phase is None:
                return {"ok":False,"reason":"not enough matched edges","iter":k,"edgesL":len(eL),"edgesR":len(eR),"matches":m,"history":hist}
            hist.append({"iter":k,"phase_ms":round(phase,1),"period_ms":round(per,1),"T":round(self.trim_fwd,4),"matches":m})
            if abs(phase) < AUTO_THRESH_MS:
                self._last_phase_ms=phase; self._last_period_ms=per; self._quality=abs(phase)
                self._save()
                return {"ok":True,"final_phase_ms":round(phase,1),"period_ms":round(per,1),"T":round(self.trim_fwd,4),"iters":k,"history":hist}
            # compute small safe step
            norm = phase / per
            delta = -AUTO_GAIN * norm
            if delta >  AUTO_STEP_MAX: delta =  AUTO_STEP_MAX
            if delta < -AUTO_STEP_MAX: delta = -AUTO_STEP_MAX
            self.trim_fwd = _clamp(self.trim_fwd + delta, -MAX_TRIM, MAX_TRIM)
            self.trim_rev = self.trim_fwd
        # final verify
        eL,eR = self._run_collect_edges(self.trim_fwd, spd, secs)
        phase, per, m = self._phase_from_edges(eL, eR)
        ok = (phase is not None) and (abs(phase) < AUTO_THRESH_MS)
        self._last_phase_ms = phase if phase is not None else None
        self._last_period_ms = per if per is not None else None
        if phase is not None: self._quality = abs(phase)
        self._save()
        return {"ok":ok,"final_phase_ms":(None if phase is None else round(phase,1)),
                "period_ms":(None if per is None else round(per,1)),
                "T":round(self.trim_fwd,4),"iters":iters,"history":hist,"matches":m}

# ===== BLE UART (NUS) optional =====
try:
    import ubluetooth as bluetooth
    HAS_BLE=True
except:
    HAS_BLE=False

class BLEUART:
    def __init__(self, name="Otto-Cal"):
        self._ble=bluetooth.BLE(); self._ble.active(True); self._ble.irq(self._irq)
        self._UUID_S=bluetooth.UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
        self._UUID_TX=bluetooth.UUID("6e400003-b5a3-f393-e0a9-e50e24dcca9e")  # notify
        self._UUID_RX=bluetooth.UUID("6e400002-b5a3-f393-e0a9-e50e24dcca9e")  # write
        self._tx=(self._UUID_TX, bluetooth.FLAG_NOTIFY)
        self._rx=(self._UUID_RX, bluetooth.FLAG_WRITE)
        ((self._txh,self._rxh),)=self._ble.gatts_register_services(((self._UUID_S,(self._tx,self._rx)),))
        self._conns=set(); self._buf=b""; self.on_line=None; self._name=name
        self._adv()
    def _adv(self, interval_us=250000):
        name=bytes(self._name,"utf-8")
        p=bytearray(b"\x02\x01\x06"); p+=bytes((len(name)+1,0x09))+name
        svc=bytes(self._UUID_S); p+=bytes((len(svc)+1,0x07))+svc
        self._ble.gap_advertise(None); self._ble.gap_advertise(interval_us,p)
    def _irq(self, evt, data):
        if evt==1: self._conns.add(data[0])
        elif evt==2: self._conns.discard(data[0]); self._adv()
        elif evt==3 and data[1]==self._rxh:
            chunk=self._ble.gatts_read(self._rxh)
            if not chunk: return
            self._buf += chunk
            while b"\n" in self._buf:
                line,self._buf=self._buf.split(b"\n",1)
                try: s=line.decode().strip()
                except: s=""
                if s and self.on_line: self.on_line(s)
    def send(self, s):
        # Send line (bytes) in <=20 byte chunks (default ATT_MTU 23 -> payload 20)
        if not isinstance(s, bytes):
            s = (s + "\n").encode()
        CHUNK = 20
        for c in list(self._conns):
            i = 0
            while i < len(s):
                try:
                    self._ble.gatts_notify(c, self._txh, s[i:i+CHUNK])
                except:
                    # Some stacks throw sporadically if flooded; brief backoff
                    try: utime.sleep_ms(10)
                    except: pass
                i += CHUNK
                try: utime.sleep_ms(5)
                except: pass

# ===== Command server (USB+BLE) =====
def send_usb(s):
    try: print(s)
    except: pass

def handle(line, send, bot):
    try:
        p=line.strip().split()
        if not p: return
        cmd=p[0]
        if cmd=="PING":
            send("PONG")
        elif cmd=="GET_STATE":
            out={
              "dir_l":bot.dir_l,"dir_r":bot.dir_r,
              "trim_fwd":bot.trim_fwd,"trim_rev":bot.trim_rev,
              "quality_ms": bot._quality,
              "last_phase_ms": bot._last_phase_ms,
              "last_period_ms": bot._last_period_ms
            }
            send("STATE "+ujson.dumps(out))
        elif cmd=="SET_DIR":
            l=int(p[1]); r=int(p[2])
            if l not in(-1,1) or r not in(-1,1):
                send("ERR SET_DIR needs -1/+1")
            else:
                bot.dir_l=l; bot.dir_r=r; bot._save(); send("OK SET_DIR {} {}".format(l,r))
        elif cmd=="SET_TRIM":
            t = _coerce_float(p[1])
            bot.trim_fwd=_clamp(t,-MAX_TRIM,MAX_TRIM)
            bot.trim_rev=bot.trim_fwd
            bot._save(); send("OK SET_TRIM {}".format(bot.trim_fwd))
        elif cmd=="MOTOR":
            l=int(p[1]); r=int(p[2]); ms=int(p[3])
            bot._write_robot(l,r); utime.sleep_ms(ms); bot.stop(); send("OK MOTOR")
        elif cmd=="TEST":
            sp=int(p[1]) if len(p)>1 else BASE_SPEED
            sec=float(p[2]) if len(p)>2 else 2.3
            res=bot.test(sp,sec); send("TEST_DONE "+ujson.dumps(res))
        elif cmd=="NUDGE_TRIM":
            phase_ms = _coerce_float(p[1]) if len(p)>1 else (bot._last_phase_ms if bot._last_phase_ms is not None else 0.0)
            gain = _coerce_float(p[2]) if len(p)>2 else NUDGE_GAIN_DEFAULT
            res=bot.nudge_trim(phase_ms, gain)
            if res.get("ok"): send("NUDGE_OK "+ujson.dumps(res))
            else: send("NUDGE_ERR "+ujson.dumps(res))
        elif cmd=="AUTO_TRIM":
            sp=int(p[1]) if len(p)>1 else BASE_SPEED
            sec=float(p[2]) if len(p)>2 else 2.0
            it=int(p[3]) if len(p)>3 else AUTO_ITERS_DEF
            res=bot.auto_trim(sp, sec, it)
            if res.get("ok"): send("AUTO_OK "+ujson.dumps(res))
            else: send("AUTO_ERR "+ujson.dumps(res))
        elif cmd=="DRIVE":
            sp=int(p[1]); sec=float(p[2]); bot.drive(sp,sec); send("OK DRIVE")
        elif cmd=="STOP":
            bot.stop(); send("OK STOP")
        else:
            send("ERR UnknownCmd")
    except Exception as e:
        try: sys.print_exception(e)
        except: pass
        try: send("ERR "+repr(e))
        except: pass

def main():
    bot=Otto()
    # BLE (optional)
    try:
        import ubluetooth as _u
        ble=BLEUART(name="Otto-Cal")
        ble.on_line=lambda s: handle(s, ble.send, bot)
        try: ble.send("READY (AUTO_TRIM | TEST | NUDGE_TRIM)")
        except: pass
    except:
        pass
    # USB
    try:
        import uselect
        poll=uselect.poll(); poll.register(sys.stdin, uselect.POLLIN)
    except:
        poll=None
    try:
        print("READY. Commands: AUTO_TRIM [spd sec iters] | TEST [spd sec] | NUDGE_TRIM phase_ms [gain] | SET_TRIM t | GET_STATE | SET_DIR l r | MOTOR l r ms | DRIVE spd sec | STOP | PING")
    except: pass
    while True:
        if poll and poll.poll(0):
            try:
                line=sys.stdin.readline()
                if line:
                    line=line.strip()
                    if line: handle(line, send_usb, bot)
            except:
                pass
        utime.sleep_ms(10)

main()

 