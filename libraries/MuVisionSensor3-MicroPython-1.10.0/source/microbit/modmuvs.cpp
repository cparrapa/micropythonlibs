/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2015-2016 Damien P. George
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <stdio.h>
#include "microbit/microbitdal.h"
#include "lib/MuVisionSensor/MuVisionSensor.h"

extern "C" {
#include "py/runtime0.h"
#include "py/runtime.h"
}

// class MuVisionSensor(object):
typedef struct {
  mp_obj_base_t base;
  MuVisionSensor* Mu;
} mu3_obj_t;

// def MuVisionSensor.__init__(self, address)
STATIC mp_obj_t mu3_make_new(const mp_obj_type_t *type,
                             size_t n_args,
                             size_t n_kw,
                             const mp_obj_t *args) {
  mp_arg_check_num(n_args, n_kw, 0, 1, false);

  mu3_obj_t *o = m_new_obj(mu3_obj_t);
  o->base.type = type;
  MuVisionSensor* Mu = nullptr;
  if (n_args) {
    uint32_t address = mp_obj_get_int(args[0]);
    Mu = new MuVisionSensor(address);
  } else {
    Mu = new MuVisionSensor();
  }
  o->Mu = Mu;
  return MP_OBJ_FROM_PTR(o);
}

// def MuVisionSensor.CameraGetAwb(self)
STATIC mp_obj_t mu3_CameraGetAwb(mp_obj_t self) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->CameraGetAwb();
  mp_obj_t ret_obj = mp_obj_new_int(ret);
  return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(mu3_camera_get_awb_obj, mu3_CameraGetAwb);

// def MuVisionSensor.CameraGetFPS(self)
STATIC mp_obj_t mu3_CameraGetFPS(mp_obj_t self) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->CameraGetFPS();
  mp_obj_t ret_obj = mp_obj_new_int(ret);
  return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(mu3_camera_get_fps_obj, mu3_CameraGetFPS);

// def MuVisionSensor.CameraGetRotate(self, enable)
STATIC mp_obj_t mu3_CameraGetRotate(mp_obj_t self) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->CameraGetRotate();
  mp_obj_t ret_obj = mp_obj_new_int(ret);
  return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(mu3_camera_get_rotate_obj, mu3_CameraGetRotate);

// def MuVisionSensor.CameraGetZoom(self, zoom)
STATIC mp_obj_t mu3_CameraGetZoom(mp_obj_t self) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->CameraGetZoom();
  mp_obj_t ret_obj = mp_obj_new_int(ret);
  return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(mu3_camera_get_zoom_obj, mu3_CameraGetZoom);

// def MuVisionSensor.CameraSetAwb(self, awb)
STATIC mp_obj_t mu3_CameraSetAwb(mp_obj_t self,
                                 mp_obj_t awb) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->CameraSetAwb(MuVsCameraWhiteBalance(mp_obj_get_int(awb)));
  mp_obj_t ret_obj = mp_obj_new_int(ret);
  return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(mu3_camera_set_awb_obj, mu3_CameraSetAwb);

// def MuVisionSensor.CameraSetFPS(self, fps)
STATIC mp_obj_t mu3_CameraSetFPS(mp_obj_t self,
                                 mp_obj_t fps) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->CameraSetFPS(MuVsCameraFPS(mp_obj_get_int(fps)));
  mp_obj_t ret_obj = mp_obj_new_int(ret);
  return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(mu3_camera_set_fps_obj, mu3_CameraSetFPS);

// def MuVisionSensor.CameraSetRotate(self, enable)
STATIC mp_obj_t mu3_CameraSetRotate(mp_obj_t self, mp_obj_t enable) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->CameraSetRotate((bool) mp_obj_get_int(enable));
  mp_obj_t ret_obj = mp_obj_new_int(ret);
  return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(mu3_camera_set_rotate_obj, mu3_CameraSetRotate);

// def MuVisionSensor.CameraSetZoom(self, zoom)
STATIC mp_obj_t mu3_CameraSetZoom(mp_obj_t self, mp_obj_t zoom) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->CameraSetZoom(MuVsCameraZoom(mp_obj_get_int(zoom)));
  mp_obj_t ret_obj = mp_obj_new_int(ret);
  return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(mu3_camera_set_zoom_obj, mu3_CameraSetZoom);

// def MuVisionSensor.GetValue(self, vision_type, object_inf)
STATIC mp_obj_t mu3_GetValue(mp_obj_t self, mp_obj_t vision_type, mp_obj_t object_inf) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->GetValue(mp_obj_get_int(vision_type), MuVsObjectInf(mp_obj_get_int(object_inf)));
  return mp_obj_new_int(ret);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_3(mu3_get_value_obj, mu3_GetValue);

// def MuVisionSensor.LEDsetColor(self, led, detected_color, undetected_color, level = 1)
STATIC mp_obj_t mu3_LedSetColor(size_t n_args, const mp_obj_t *args) {
  mu3_obj_t *p = (mu3_obj_t*) args[0];
  mu_err_t err;
  if (n_args == 5) {
    err = p->Mu->LedSetColor(MuVsLed(mp_obj_get_int(args[1])),
                              MuVsLedColor(mp_obj_get_int(args[2])),
                              MuVsLedColor(mp_obj_get_int(args[3])),
                              mp_obj_get_int(args[4]));
  } else {
    err = p->Mu->LedSetColor(MuVsLed(mp_obj_get_int(args[1])),
                              MuVsLedColor(mp_obj_get_int(args[2])),
                              MuVsLedColor(mp_obj_get_int(args[3])));
  }
  return mp_obj_new_int(err);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(mu3_led_set_color_obj, 4, 5, mu3_LedSetColor);

// def MuVisionSensor.LEDsetMode(self, led, manual, hold)
STATIC mp_obj_t mu3_LedSetMode(size_t n_args, const mp_obj_t *args) {
  n_args = sizeof(n_args);
  mu3_obj_t *p = (mu3_obj_t*) args[0];
  p->Mu->LedSetMode(MuVsLed(mp_obj_get_int(args[1])),
                    bool(mp_obj_get_int(args[2])),
                    bool(mp_obj_get_int(args[3])));
  return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(mu3_led_set_mode_obj, 4, 4, mu3_LedSetMode);

// def MuVisionSensor.SensorSetDefault(self)
STATIC mp_obj_t mu3_SensorSetDefault(mp_obj_t self) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  p->Mu->SensorSetDefault();
  return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(mu3_sensor_set_default_obj, mu3_SensorSetDefault);

// def MuVisionSensor.SensorSetRestart(self)
STATIC mp_obj_t mu3_SensorSetRestart(mp_obj_t self) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  p->Mu->SensorSetRestart();
  return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(mu3_sensor_set_restart_obj, mu3_SensorSetRestart);

// def MuVisionSensor.SetValue(self, vision_type, object_inf, value)
STATIC mp_obj_t mu3_SetValue(size_t n_args, const mp_obj_t *args) {
  n_args = sizeof(n_args);
  mu3_obj_t *p = (mu3_obj_t*) args[0];
  mu_err_t err = p->Mu->SetValue(mp_obj_get_int(args[1]),
                  MuVsObjectInf(mp_obj_get_int(args[2])),
                  mp_obj_get_int(args[3]));
  return mp_obj_new_int(err);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(mu3_set_value_obj, 4, 4, mu3_SetValue);

// def MuVisionSensor.UartSetBaudrate(self, baudrate)
//STATIC mp_obj_t mu3_UartSetBaudrate(mp_obj_t self, mp_obj_t baudrate) { //<! XXX UART mode only
//  mu3_obj_t *p = (mu3_obj_t*) self;
//  mu_err_t err = p->Mu->UartSetBaudrate(MuVsBaudrate(mp_obj_get_int(baudrate)));
//  return mp_obj_new_int(err);
//}
//STATIC MP_DEFINE_CONST_FUN_OBJ_2(mu3_uart_set_baudrate_obj, mu3_UartSetBaudrate);

// def MuVisionSensor.UpdateResult(self, vision_type, wait_all_result)
STATIC mp_obj_t mu3_UpdateResult(size_t n_args, const mp_obj_t *args) {
  mu3_obj_t *p = (mu3_obj_t*) args[0];
  MuVisionType vision_type;
  if (n_args == 3) {
    vision_type = p->Mu->UpdateResult(mp_obj_get_int(args[1]), mp_obj_get_int(args[2]));
  } else {
    vision_type = p->Mu->UpdateResult(mp_obj_get_int(args[1]));
  }
  return mp_obj_new_int(vision_type);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(mu3_update_result_obj, 2, 3, mu3_UpdateResult);

// def MuVisionSensor.VisionBegin(self, vision_type)
STATIC mp_obj_t mu3_VisionBegin(mp_obj_t self, mp_obj_t vision_type) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  mu_err_t err = p->Mu->VisionBegin(mp_obj_get_int(vision_type));
  return mp_obj_new_int(err);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(mu3_vision_begin_obj, mu3_VisionBegin);

// def MuVisionSensor.VisionEnd(self, vision_type)
STATIC mp_obj_t mu3_VisionEnd(mp_obj_t self, mp_obj_t vision_type) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  mu_err_t err = p->Mu->VisionEnd(mp_obj_get_int(vision_type));
  return mp_obj_new_int(err);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(mu3_vision_end_obj, mu3_VisionEnd);

// def MuVisionSensor.VisionGetLevel(self, vision_type)
STATIC mp_obj_t mu3_VisionGetLevel(mp_obj_t self, mp_obj_t vision_type) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->VisionGetLevel(mp_obj_get_int(vision_type));
  mp_obj_t ret_obj = mp_obj_new_int(ret);
  return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(mu3_vision_get_level_obj, mu3_VisionGetLevel);

// def MuVisionSensor.VisionGetOutputMode(self) //<! XXX UART mode only
//STATIC mp_obj_t mu3_VisionGetOutputMode(mp_obj_t self) {
//  mu3_obj_t *p = (mu3_obj_t*) self;
//  int ret = p->Mu->VisionGetOutputMode();
//  mp_obj_t ret_obj = mp_obj_new_int(ret);
//  return ret_obj;
//}
//STATIC MP_DEFINE_CONST_FUN_OBJ_1(mu3_vision_get_outputMode_obj, mu3_VisionGetOutputMode);

// def MuVisionSensor.VisionGetStatus(self, vision_type)
STATIC mp_obj_t mu3_VisionGetStatus(mp_obj_t self, mp_obj_t vision_type) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->VisionGetStatus(mp_obj_get_int(vision_type));
  mp_obj_t ret_obj = mp_obj_new_int(ret);
  return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(mu3_vision_get_status_obj, mu3_VisionGetStatus);

// def MuVisionSensor.VisionSetDefault(self, vision_type)
STATIC mp_obj_t mu3_VisionSetDefault(mp_obj_t self, mp_obj_t vision_type) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  mu_err_t err = p->Mu->VisionSetDefault(mp_obj_get_int(vision_type));
  return mp_obj_new_int(err);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(mu3_vision_set_default_obj, mu3_VisionSetDefault);

// def MuVisionSensor.VisionSetLevel(self, vision_type, level)
STATIC mp_obj_t mu3_VisionSetLevel(mp_obj_t self, mp_obj_t vision_type, mp_obj_t level) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  int ret = p->Mu->VisionSetLevel(mp_obj_get_int(vision_type),
                                  MuVsVisionLevel(mp_obj_get_int(level)));
  mp_obj_t ret_obj = mp_obj_new_int(ret);
  return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_3(mu3_vision_set_level_obj, mu3_VisionSetLevel);

// def MuVisionSensor.VisionSetOutputEnable(self, vision_type, status)
//STATIC mp_obj_t mod_muvs_MuVisionSensor_VisionSetOutputEnable(mp_obj_t self,
//                                                              mp_obj_t vision_type,
//                                                              mp_obj_t status) {
//  // XXX UART mode only
//  mu3_obj_t *p = (mu3_obj_t*) self;
//  mu_err_t err = p->Mu->VisionSetOutputEnable(mp_obj_get_int(vision_type), mp_obj_get_int(status));
//  return mp_obj_new_int(err);
//}
//STATIC MP_DEFINE_CONST_FUN_OBJ_3(mod_muvs_MuVisionSensor_VisionSetOutputEnable_obj, mod_muvs_MuVisionSensor_VisionSetOutputEnable);

// def MuVisionSensor.VisionSetOutputMode(self, mode)
//STATIC mp_obj_t mod_muvs_MuVisionSensor_VisionSetOutputMode(mp_obj_t self,
//                                                            mp_obj_t mode) {
//  // XXX UART mode only
//  mu3_obj_t *p = (mu3_obj_t*) self;
//  mu_err_t err = p->Mu->VisionSetOutputMode(MuVsStreamOutputMode(mp_obj_get_int(mode)));
//  return mp_obj_new_int(err);
//}
//STATIC MP_DEFINE_CONST_FUN_OBJ_2(mod_muvs_MuVisionSensor_VisionSetOutputMode_obj, mod_muvs_MuVisionSensor_VisionSetOutputMode);

// def MuVisionSensor.VisionSetStatus(self, vision_type, enable)
STATIC mp_obj_t mu3_VisionSetStatus(mp_obj_t self,
                                    mp_obj_t vision_type,
                                    mp_obj_t enable) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  mu_err_t err = p->Mu->VisionSetStatus(mp_obj_get_int(vision_type), mp_obj_get_int(enable));
  return mp_obj_new_int(err);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_3(mu3_vision_set_status_obj, mu3_VisionSetStatus);

// def MuVisionSensor.begin(self, communication_port, mode)
STATIC mp_obj_t mu3_begin(mp_obj_t self) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  mu_err_t err = p->Mu->begin(&ubit_i2c);
  return mp_obj_new_int(err);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(mu3_begin_obj, mu3_begin);

// def MuVisionSensor.read(self, vision_type, object_inf, result_num=1)
STATIC mp_obj_t mu3_read(size_t n_args, const mp_obj_t *args) {
  n_args = sizeof(n_args);
  mu3_obj_t *p = (mu3_obj_t*) args[0];
  int ret;
  if (n_args == 4) {
    ret = p->Mu->read(mp_obj_get_int(args[1]),
                      MuVsObjectInf(mp_obj_get_int(args[2])),
                      mp_obj_get_int(args[3]));
  } else if (n_args == 3) {
    ret = p->Mu->read(mp_obj_get_int(args[1]), MuVsObjectInf(mp_obj_get_int(args[2])));
  }
  return mp_obj_new_int(ret);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(mu3_read_obj, 3, 4, mu3_read);

// def MuVisionSensor.write(self, vision_type, object_inf, value)
STATIC mp_obj_t mu3_write(size_t n_args, const mp_obj_t *args) {
  n_args = sizeof(n_args);
  mu3_obj_t *p = (mu3_obj_t*) args[0];
  mu_err_t err = p->Mu->write(mp_obj_get_int(args[1]),
                              MuVsObjectInf(mp_obj_get_int(args[2])),
                              mp_obj_get_int(args[3]));
  return mp_obj_new_int(err);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(mu3_write_obj, 4, 4, mu3_write);

// def MuVisionSensor.write(self, vision_type, object_inf, value)
STATIC mp_obj_t mu3_LsBegin(mp_obj_t self,
                            mp_obj_t ls_type) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  mu_err_t err = p->Mu->LsBegin(MuLightSensorType(mp_obj_get_int(ls_type)));
  return mp_obj_new_int(err);
}
MP_DEFINE_CONST_FUN_OBJ_2(mu3_ls_begin_obj, mu3_LsBegin);

// def MuVisionSensor.LsEnd(self, ls_type)
STATIC mp_obj_t mu3_LsEnd(mp_obj_t self,
                          mp_obj_t ls_type) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  mu_err_t err = p->Mu->LsEnd(MuLightSensorType(mp_obj_get_int(ls_type)));
  return mp_obj_new_int(err);
}
MP_DEFINE_CONST_FUN_OBJ_2(mu3_ls_end_obj, mu3_LsEnd);

// def MuVisionSensor.LsSetSensitivity(self, sensitivity)
STATIC mp_obj_t mu3_LsSetSensitivity(mp_obj_t self,
                                     mp_obj_t sensitivity) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  mu_err_t err = p->Mu->LsSetSensitivity(MuVsLsSensitivity(mp_obj_get_int(sensitivity)));
  return mp_obj_new_int(err);
}
MP_DEFINE_CONST_FUN_OBJ_2(mu3_ls_set_sensitivity_obj, mu3_LsSetSensitivity);

// def MuVisionSensor.LsWhiteBalanceEnable(self)
STATIC mp_obj_t mu3_LsWhiteBalanceEnable(mp_obj_t self) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  mu_err_t err = p->Mu->LsWhiteBalanceEnable();
  return mp_obj_new_int(err);
}
MP_DEFINE_CONST_FUN_OBJ_1(mu3_ls_white_balance_enable_obj, mu3_LsWhiteBalanceEnable);

// def MuVisionSensor.LsReadProximity(self)
STATIC mp_obj_t mu3_LsReadProximity(mp_obj_t self) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  uint8_t proximity = p->Mu->LsReadProximity();
  return mp_obj_new_int(proximity);
}
MP_DEFINE_CONST_FUN_OBJ_1(mu3_ls_read_proximity_obj, mu3_LsReadProximity);

// def MuVisionSensor.LsReadAmbientLight(self)
STATIC mp_obj_t mu3_LsReadAmbientLight(mp_obj_t self) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  uint16_t als = p->Mu->LsReadAmbientLight();
  return mp_obj_new_int(als);
}
MP_DEFINE_CONST_FUN_OBJ_1(mu3_ls_read_ambient_light_obj, mu3_LsReadAmbientLight);

// def MuVisionSensor.LsReadColor(self, color_t)
STATIC mp_obj_t mu3_LsReadColor(mp_obj_t self,
                                mp_obj_t color_t) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  uint16_t color = p->Mu->LsReadColor(MuVsLsColorType(mp_obj_get_int(color_t)));
  return mp_obj_new_int(color);
}
MP_DEFINE_CONST_FUN_OBJ_2(mu3_ls_read_color_obj, mu3_LsReadColor);

// def MuVisionSensor.LsReadRawColor(self, color_t)
STATIC mp_obj_t mu3_LsReadRawColor(mp_obj_t self,
                                   mp_obj_t color_t) {
  String str = "asdad";
  mu3_obj_t *p = (mu3_obj_t*) self;
  uint16_t color = p->Mu->LsReadRawColor(MuVsLsRawColorType(mp_obj_get_int(color_t)));
  return mp_obj_new_int(color);
}
MP_DEFINE_CONST_FUN_OBJ_2(mu3_ls_read_raw_color_obj, mu3_LsReadRawColor);

// def MuVisionSensor.LsReadGesture(self)
STATIC mp_obj_t mu3_LsReadGesture(mp_obj_t self) {
  mu3_obj_t *p = (mu3_obj_t*) self;
  MuVsLsGesture gesture = p->Mu->LsReadGesture();
  return mp_obj_new_int(gesture);
}
MP_DEFINE_CONST_FUN_OBJ_1(mu3_ls_read_gesture_obj, mu3_LsReadGesture);

// MuVisionSensor stuff
STATIC const mp_rom_map_elem_t mu3_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_CameraGetAwb), MP_ROM_PTR(&mu3_camera_get_awb_obj) },
    { MP_ROM_QSTR(MP_QSTR_CameraGetFPS), MP_ROM_PTR(&mu3_camera_get_fps_obj) },
    { MP_ROM_QSTR(MP_QSTR_CameraGetRotate), MP_ROM_PTR(&mu3_camera_get_rotate_obj) },
    { MP_ROM_QSTR(MP_QSTR_CameraGetZoom), MP_ROM_PTR(&mu3_camera_get_zoom_obj) },
    { MP_ROM_QSTR(MP_QSTR_CameraSetAwb), MP_ROM_PTR(&mu3_camera_set_awb_obj) },
    { MP_ROM_QSTR(MP_QSTR_CameraSetFPS), MP_ROM_PTR(&mu3_camera_set_fps_obj) },
    { MP_ROM_QSTR(MP_QSTR_CameraSetRotate), MP_ROM_PTR(&mu3_camera_set_rotate_obj) },
    { MP_ROM_QSTR(MP_QSTR_CameraSetZoom), MP_ROM_PTR(&mu3_camera_set_zoom_obj) },
    { MP_ROM_QSTR(MP_QSTR_GetValue), MP_ROM_PTR(&mu3_get_value_obj) },
    { MP_ROM_QSTR(MP_QSTR_LedSetColor), MP_ROM_PTR(&mu3_led_set_color_obj) },
    { MP_ROM_QSTR(MP_QSTR_LedSetMode), MP_ROM_PTR(&mu3_led_set_mode_obj) },
    { MP_ROM_QSTR(MP_QSTR_SensorSetDefault), MP_ROM_PTR(&mu3_sensor_set_default_obj) },
    { MP_ROM_QSTR(MP_QSTR_SensorSetRestart), MP_ROM_PTR(&mu3_sensor_set_restart_obj) },
    { MP_ROM_QSTR(MP_QSTR_SetValue), MP_ROM_PTR(&mu3_set_value_obj) },
//    { MP_ROM_QSTR(MP_QSTR_UartSetBaudrate), MP_ROM_PTR(&mod_muvs_MuVisionSensor_UartSetBaudrate_obj) },   //<! XXX UART mode only
    { MP_ROM_QSTR(MP_QSTR_UpdateResult), MP_ROM_PTR(&mu3_update_result_obj) },
    { MP_ROM_QSTR(MP_QSTR_VisionBegin), MP_ROM_PTR(&mu3_vision_begin_obj) },
    { MP_ROM_QSTR(MP_QSTR_VisionEnd), MP_ROM_PTR(&mu3_vision_end_obj) },
    { MP_ROM_QSTR(MP_QSTR_VisionGetLevel), MP_ROM_PTR(&mu3_vision_get_level_obj) },
//    { MP_ROM_QSTR(MP_QSTR_VisionGetOutputMode), MP_ROM_PTR(&mu3_vision_get_outputMode_obj) },   //<! XXX UART mode only
    { MP_ROM_QSTR(MP_QSTR_VisionGetStatus), MP_ROM_PTR(&mu3_vision_get_status_obj) },
    { MP_ROM_QSTR(MP_QSTR_VisionSetDefault), MP_ROM_PTR(&mu3_vision_set_default_obj) },
    { MP_ROM_QSTR(MP_QSTR_VisionSetLevel), MP_ROM_PTR(&mu3_vision_set_level_obj) },
//    { MP_ROM_QSTR(MP_QSTR_VisionSetOutputEnable), MP_ROM_PTR(&mod_muvs_MuVisionSensor_VisionSetOutputEnable_obj) }, //<! XXX UART mode only
//    { MP_ROM_QSTR(MP_QSTR_VisionSetOutputMode), MP_ROM_PTR(&mod_muvs_MuVisionSensor_VisionSetOutputMode_obj) },     //<! XXX UART mode only
    { MP_ROM_QSTR(MP_QSTR_VisionSetStatus), MP_ROM_PTR(&mu3_vision_set_status_obj) },
    { MP_ROM_QSTR(MP_QSTR_begin), MP_ROM_PTR(&mu3_begin_obj) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&mu3_read_obj) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&mu3_write_obj) },
    // light sensor function
    { MP_ROM_QSTR(MP_QSTR_LsBegin), MP_ROM_PTR(&mu3_ls_begin_obj) },
    { MP_ROM_QSTR(MP_QSTR_LsEnd), MP_ROM_PTR(&mu3_ls_end_obj) },
    { MP_ROM_QSTR(MP_QSTR_LsSetSensitivity), MP_ROM_PTR(&mu3_ls_set_sensitivity_obj) },
    { MP_ROM_QSTR(MP_QSTR_LsWhiteBalanceEnable), MP_ROM_PTR(&mu3_ls_white_balance_enable_obj) },
    { MP_ROM_QSTR(MP_QSTR_LsReadProximity), MP_ROM_PTR(&mu3_ls_read_proximity_obj) },
    { MP_ROM_QSTR(MP_QSTR_LsReadAmbientLight), MP_ROM_PTR(&mu3_ls_read_ambient_light_obj) },
    { MP_ROM_QSTR(MP_QSTR_LsReadColor), MP_ROM_PTR(&mu3_ls_read_color_obj) },
    { MP_ROM_QSTR(MP_QSTR_LsReadRawColor), MP_ROM_PTR(&mu3_ls_read_raw_color_obj) },
    { MP_ROM_QSTR(MP_QSTR_LsReadGesture), MP_ROM_PTR(&mu3_ls_read_gesture_obj) },
};
STATIC MP_DEFINE_CONST_DICT(mu3_locals_dict, mu3_locals_dict_table);

STATIC const mp_obj_type_t mu3_type = {
    { &mp_type_type },
    .name = MP_QSTR_MuVisionSensor,
    .print = NULL,
    .make_new = mu3_make_new,
    .call = NULL,
    .unary_op = NULL,
    .binary_op = NULL,
    .attr = NULL,
    .subscr = NULL,
    .getiter = NULL,
    .iternext = NULL,
    .buffer_p = {NULL},
    .protocol = NULL,
    .parent = NULL,
    .locals_dict = (mp_obj_dict_t*)&mu3_locals_dict,
};

// module stuff
STATIC const mp_rom_map_elem_t mu3_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_MuVisionSensor) },
    { MP_ROM_QSTR(MP_QSTR_MuVisionSensor), MP_ROM_PTR(&mu3_type) },
    // XXX enum MuVsMode, UART mode only
//    { MP_ROM_QSTR(MP_QSTR_I2C), MP_ROM_INT(1) },
//    { MP_ROM_QSTR(MP_QSTR_Serial), MP_ROM_INT(0) },
    // def MuVisionType
    { MP_ROM_QSTR(MP_QSTR_VISION_COLOR_DETECT), MP_ROM_INT(VISION_COLOR_DETECT) },
    { MP_ROM_QSTR(MP_QSTR_VISION_COLOR_RECOGNITION), MP_ROM_INT(VISION_COLOR_RECOGNITION) },
    { MP_ROM_QSTR(MP_QSTR_VISION_BALL_DETECT), MP_ROM_INT(VISION_BALL_DETECT) },
    { MP_ROM_QSTR(MP_QSTR_VISION_BODY_DETECT), MP_ROM_INT(VISION_BODY_DETECT) },
    { MP_ROM_QSTR(MP_QSTR_VISION_SHAPE_CARD_DETECT), MP_ROM_INT(VISION_SHAPE_CARD_DETECT) },
    { MP_ROM_QSTR(MP_QSTR_VISION_TRAFFIC_CARD_DETECT), MP_ROM_INT(VISION_TRAFFIC_CARD_DETECT) },
    { MP_ROM_QSTR(MP_QSTR_VISION_NUM_CARD_DETECT), MP_ROM_INT(VISION_NUM_CARD_DETECT) },
    { MP_ROM_QSTR(MP_QSTR_VISION_ALL), MP_ROM_INT(VISION_ALL) },
    // def MuLightSensorType
    { MP_ROM_QSTR(MP_QSTR_LS_PROXIMITY_ENABLE), MP_ROM_INT(LS_PROXIMITY_ENABLE) },
    { MP_ROM_QSTR(MP_QSTR_LS_AMBIENT_LIGHT_ENABLE), MP_ROM_INT(LS_AMBIENT_LIGHT_ENABLE) },
    { MP_ROM_QSTR(MP_QSTR_LS_COLOR_ENABLE), MP_ROM_INT(LS_COLOR_ENABLE) },
    { MP_ROM_QSTR(MP_QSTR_LS_GESTURE_ENABLE), MP_ROM_INT(LS_GESTURE_ENABLE) },
    // def Vision Shape Card
    { MP_ROM_QSTR(MP_QSTR_MU_SHAPE_CARD_TICK), MP_ROM_INT(MU_SHAPE_CARD_TICK) },
    { MP_ROM_QSTR(MP_QSTR_MU_SHAPE_CARD_CROSS), MP_ROM_INT(MU_SHAPE_CARD_CROSS) },
    { MP_ROM_QSTR(MP_QSTR_MU_SHAPE_CARD_CIRCLE), MP_ROM_INT(MU_SHAPE_CARD_CIRCLE) },
    { MP_ROM_QSTR(MP_QSTR_MU_SHAPE_CARD_SQUARE), MP_ROM_INT(MU_SHAPE_CARD_SQUARE) },
    { MP_ROM_QSTR(MP_QSTR_MU_SHAPE_CARD_TRIANGLE), MP_ROM_INT(MU_SHAPE_CARD_TRIANGLE) },
    // def Vision Traffic Card
    { MP_ROM_QSTR(MP_QSTR_MU_TRAFFIC_CARD_FORWARD), MP_ROM_INT(MU_TRAFFIC_CARD_FORWARD) },
    { MP_ROM_QSTR(MP_QSTR_MU_TRAFFIC_CARD_LEFT), MP_ROM_INT(MU_TRAFFIC_CARD_LEFT) },
    { MP_ROM_QSTR(MP_QSTR_MU_TRAFFIC_CARD_RIGHT), MP_ROM_INT(MU_TRAFFIC_CARD_RIGHT) },
    { MP_ROM_QSTR(MP_QSTR_MU_TRAFFIC_CARD_TURN_AROUND), MP_ROM_INT(MU_TRAFFIC_CARD_TURN_AROUND) },
    { MP_ROM_QSTR(MP_QSTR_MU_TRAFFIC_CARD_PARK), MP_ROM_INT(MU_TRAFFIC_CARD_PARK) },
    // def Vision Color Type
    { MP_ROM_QSTR(MP_QSTR_MU_COLOR_UNKNOWN), MP_ROM_INT(MU_COLOR_UNKNOWN) },
    { MP_ROM_QSTR(MP_QSTR_MU_COLOR_BLACK), MP_ROM_INT(MU_COLOR_BLACK) },
    { MP_ROM_QSTR(MP_QSTR_MU_COLOR_WHITE), MP_ROM_INT(MU_COLOR_WHITE) },
    { MP_ROM_QSTR(MP_QSTR_MU_COLOR_RED), MP_ROM_INT(MU_COLOR_RED) },
    { MP_ROM_QSTR(MP_QSTR_MU_COLOR_YELLOW), MP_ROM_INT(MU_COLOR_YELLOW) },
    { MP_ROM_QSTR(MP_QSTR_MU_COLOR_GREEN), MP_ROM_INT(MU_COLOR_GREEN) },
    { MP_ROM_QSTR(MP_QSTR_MU_COLOR_CYAN), MP_ROM_INT(MU_COLOR_CYAN) },
    { MP_ROM_QSTR(MP_QSTR_MU_COLOR_BLUE), MP_ROM_INT(MU_COLOR_BLUE) },
    { MP_ROM_QSTR(MP_QSTR_MU_COLOR_PURPLE), MP_ROM_INT(MU_COLOR_PURPLE) },
    // XXX enum MuVsBaudrate, UART mode only
//    { MP_ROM_QSTR(MP_QSTR_Baud9600), MP_ROM_INT(kBaud9600) },
//    { MP_ROM_QSTR(MP_QSTR_Baud19200), MP_ROM_INT(kBaud19200) },
//    { MP_ROM_QSTR(MP_QSTR_Baud38400), MP_ROM_INT(kBaud38400) },
//    { MP_ROM_QSTR(MP_QSTR_Baud57600), MP_ROM_INT(kBaud57600) },
//    { MP_ROM_QSTR(MP_QSTR_Baud115200), MP_ROM_INT(kBaud115200) },
//    { MP_ROM_QSTR(MP_QSTR_Baud230400), MP_ROM_INT(kBaud230400) },
//    { MP_ROM_QSTR(MP_QSTR_Baud460800), MP_ROM_INT(kBaud460800) },
//    { MP_ROM_QSTR(MP_QSTR_Baud921600), MP_ROM_INT(kBaud921600) },
    // enum MuVsObjectInf
    { MP_ROM_QSTR(MP_QSTR_Status), MP_ROM_INT(kStatus) },
    { MP_ROM_QSTR(MP_QSTR_XValue), MP_ROM_INT(kXValue) },
    { MP_ROM_QSTR(MP_QSTR_YValue), MP_ROM_INT(kYValue) },
    { MP_ROM_QSTR(MP_QSTR_WidthValue), MP_ROM_INT(kWidthValue) },
    { MP_ROM_QSTR(MP_QSTR_HeightValue), MP_ROM_INT(kHeightValue) },
    { MP_ROM_QSTR(MP_QSTR_Label), MP_ROM_INT(kLabel) },
    { MP_ROM_QSTR(MP_QSTR_RValue), MP_ROM_INT(kRValue) },
    { MP_ROM_QSTR(MP_QSTR_GValue), MP_ROM_INT(kGValue) },
    { MP_ROM_QSTR(MP_QSTR_BValue), MP_ROM_INT(kBValue) },
    // XXX enum MuVsStreamOutputMode, UART mode only
//    { MP_ROM_QSTR(MP_QSTR_CallBackMode), MP_ROM_INT(kCallBackMode) },
//    { MP_ROM_QSTR(MP_QSTR_DataFlowMode), MP_ROM_INT(kDataFlowMode) },
//    { MP_ROM_QSTR(MP_QSTR_EventMode), MP_ROM_INT(kEventMode) },
    // enum MuVsCameraZoom
    { MP_ROM_QSTR(MP_QSTR_ZoomDefault), MP_ROM_INT(kZoomDefault) },
    { MP_ROM_QSTR(MP_QSTR_Zoom1), MP_ROM_INT(kZoom1) },
    { MP_ROM_QSTR(MP_QSTR_Zoom2), MP_ROM_INT(kZoom2) },
    { MP_ROM_QSTR(MP_QSTR_Zoom3), MP_ROM_INT(kZoom3) },
    { MP_ROM_QSTR(MP_QSTR_Zoom4), MP_ROM_INT(kZoom4) },
    { MP_ROM_QSTR(MP_QSTR_Zoom5), MP_ROM_INT(kZoom5) },
    // enum MuVsCameraFPS
    { MP_ROM_QSTR(MP_QSTR_FPSNormal), MP_ROM_INT(kFPSNormal) },
    { MP_ROM_QSTR(MP_QSTR_FPSHigh), MP_ROM_INT(kFPSHigh) },
    // enum MuVsCameraWhiteBalance
    { MP_ROM_QSTR(MP_QSTR_AutoWhiteBalance), MP_ROM_INT(kAutoWhiteBalance) },
    { MP_ROM_QSTR(MP_QSTR_LockWhiteBalance), MP_ROM_INT(kLockWhiteBalance) },
    { MP_ROM_QSTR(MP_QSTR_WhiteLight), MP_ROM_INT(kWhiteLight) },
    { MP_ROM_QSTR(MP_QSTR_YellowLight), MP_ROM_INT(kYellowLight) },
    // enum MuVsVisionLevel
    { MP_ROM_QSTR(MP_QSTR_LevelDefault), MP_ROM_INT(kLevelDefault) },
    { MP_ROM_QSTR(MP_QSTR_LevelSpeed), MP_ROM_INT(kLevelSpeed) },
    { MP_ROM_QSTR(MP_QSTR_LevelBalance), MP_ROM_INT(kLevelBalance) },
    { MP_ROM_QSTR(MP_QSTR_LevelAccuracy), MP_ROM_INT(kLevelAccuracy) },
    // enum MuVsLsSensitivity
    { MP_ROM_QSTR(MP_QSTR_SensitivityDefault), MP_ROM_INT(kSensitivityDefault) },
    { MP_ROM_QSTR(MP_QSTR_Sensitivity1), MP_ROM_INT(kSensitivity1) },
    { MP_ROM_QSTR(MP_QSTR_Sensitivity2), MP_ROM_INT(kSensitivity2) },
    { MP_ROM_QSTR(MP_QSTR_Sensitivity3), MP_ROM_INT(kSensitivity3) },
    // enum MuVsLsGesture
    { MP_ROM_QSTR(MP_QSTR_GestureNone), MP_ROM_INT(kGestureNone) },
    { MP_ROM_QSTR(MP_QSTR_GestureUp), MP_ROM_INT(kGestureUp) },
    { MP_ROM_QSTR(MP_QSTR_GestureDown), MP_ROM_INT(kGestureDown) },
    { MP_ROM_QSTR(MP_QSTR_GestureLeft), MP_ROM_INT(kGestureLeft) },
    { MP_ROM_QSTR(MP_QSTR_GestureRight), MP_ROM_INT(kGestureRight) },
    { MP_ROM_QSTR(MP_QSTR_GesturePush), MP_ROM_INT(kGesturePush) },
    { MP_ROM_QSTR(MP_QSTR_GesturePull), MP_ROM_INT(kGesturePull) },
    // enum MuVsLsColorType
    { MP_ROM_QSTR(MP_QSTR_LsColorLabel), MP_ROM_INT(kLsColorLabel) },
    { MP_ROM_QSTR(MP_QSTR_LsColorRed), MP_ROM_INT(kLsColorRed) },
    { MP_ROM_QSTR(MP_QSTR_LsColorGreen), MP_ROM_INT(kLsColorGreen) },
    { MP_ROM_QSTR(MP_QSTR_LsColorBlue), MP_ROM_INT(kLsColorBlue) },
    { MP_ROM_QSTR(MP_QSTR_LsColorHue), MP_ROM_INT(kLsColorHue) },
    { MP_ROM_QSTR(MP_QSTR_LsColorSaturation), MP_ROM_INT(kLsColorSaturation) },
    { MP_ROM_QSTR(MP_QSTR_LsColorValue), MP_ROM_INT(kLsColorValue) },
    // enum MuVsLsRawColorType
    { MP_ROM_QSTR(MP_QSTR_LsRawColorRed), MP_ROM_INT(kLsRawColorRed) },
    { MP_ROM_QSTR(MP_QSTR_LsRawColorGreen), MP_ROM_INT(kLsRawColorGreen) },
    { MP_ROM_QSTR(MP_QSTR_LsRawColorBlue), MP_ROM_INT(kLsRawColorBlue) },
    // enum MuVsLed
    { MP_ROM_QSTR(MP_QSTR_Led1), MP_ROM_INT(kLed1) },
    { MP_ROM_QSTR(MP_QSTR_Led2), MP_ROM_INT(kLed2) },
    { MP_ROM_QSTR(MP_QSTR_LedAll), MP_ROM_INT(kLedAll) },
    // enum MuVsLedColor
    { MP_ROM_QSTR(MP_QSTR_LedClose), MP_ROM_INT(kLedClose) },
    { MP_ROM_QSTR(MP_QSTR_LedRed), MP_ROM_INT(kLedRed) },
    { MP_ROM_QSTR(MP_QSTR_LedGreen), MP_ROM_INT(kLedGreen) },
    { MP_ROM_QSTR(MP_QSTR_LedYellow), MP_ROM_INT(kLedYellow) },
    { MP_ROM_QSTR(MP_QSTR_LedBlue), MP_ROM_INT(kLedBlue) },
    { MP_ROM_QSTR(MP_QSTR_LedPurple), MP_ROM_INT(kLedPurple) },
    { MP_ROM_QSTR(MP_QSTR_LedCyan), MP_ROM_INT(kLedCyan) },
    { MP_ROM_QSTR(MP_QSTR_LedWhite), MP_ROM_INT(kLedWhite) },
};
STATIC MP_DEFINE_CONST_DICT(mu3_module_globals, mu3_module_globals_table);

const mp_obj_module_t mp_module_muvs = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&mu3_module_globals,
};
