import urandom # type: ignore
from servo_lib import RobotConfig, ServoController, NeutralPositions, RobotReceiver
from moves import RobotMoves
import time

cfg    = RobotConfig()
servos = cfg.servos
robot  = cfg.robot

npos = NeutralPositions() # neutral positions

RF, RL, RA = cfg.RF, cfg.RL, cfg.RA
LF, LL, LA = cfg.LF, cfg.LL, cfg.LA

moves = RobotMoves(servos, LF, RF, LL, RL, LA, RA)


def main():
    while True:
        if cfg.tick():
            servos.speed_multiplier = robot.pot1 / 100.0 # ograniczenie prędkości serw 360 stopni

            cfg.handle_button_state(
                'sw3',
                robot.sw3,
                moves.ride_position,
                lambda: servos.move_to_angles(LL, npos.LLN, RL, npos.RLN, step=10, delay=0.02),  # szybki powrót do pozycji neutralnej dla stabilności
            )

            cfg.handle_button_state(
                'sw4',
                robot.sw4,
                moves.ride_position,
                lambda: servos.move_to_angles(LL, npos.LLN, RL, npos.RLN, step=10, delay=0.02),  # szybki powrót do pozycji neutralnej dla stabilności
            )

            if cfg.button_states['sw3']:
                servos.set_speed(LF, ServoController.map_joystick(robot.ly, npos.JOY_DEAD, npos.LF_SERVO_MIN, npos.LF_SERVO_MAX))
                servos.set_speed(RF, ServoController.map_joystick(-robot.ry, npos.JOY_DEAD, npos.RF_SERVO_MIN, npos.RF_SERVO_MAX))

            if cfg.button_states['sw4']:
                # Sterowanie rozdzielone (przód/tył, skręt)
                forward = robot.ly
                turn = robot.rx * npos.turn_sensitivity
                servos.set_speed(LF, ServoController.map_joystick(forward + turn, npos.JOY_DEAD, npos.LF_SERVO_MIN, npos.LF_SERVO_MAX))
                servos.set_speed(RF, ServoController.map_joystick(-(forward - turn), npos.JOY_DEAD, npos.RF_SERVO_MIN, npos.RF_SERVO_MAX))

            screen = robot.screen

            if screen == RobotReceiver.SCREEN_2:
                cfg.handle_button_state('bt1', robot.bt1, moves.steps)
                cfg.handle_button_state('bt2', robot.bt2, moves.arms)
                cfg.handle_button_state('bt3', robot.bt3, moves.left_back, moves.return_to_neutral)
                cfg.handle_button_state('bt4', robot.bt4, moves.left_forward, moves.return_to_neutral)
                cfg.handle_button_state('bt5', robot.bt5, moves.tilt)
                cfg.handle_button_state('bt6', robot.bt6, moves.wave)
                cfg.handle_button_state('bt7', robot.bt7, moves.right_back, moves.return_to_neutral)
                cfg.handle_button_state('bt8', robot.bt8, moves.right_forward, moves.return_to_neutral)

            elif screen == RobotReceiver.SCREEN_3:
                cfg.handle_button_state('bt1', robot.bt1, moves.weird)
                cfg.handle_button_state('bt2', robot.bt2, moves.balerina, moves.return_to_neutral)
                cfg.handle_button_state('bt3', robot.bt3, moves.boogie)
                cfg.handle_button_state('bt4', robot.bt4, moves.spin)
                cfg.handle_button_state('bt5', robot.bt5, moves.toes)
                cfg.handle_button_state('bt6', robot.bt6, moves.step_left)
                cfg.handle_button_state('bt7', robot.bt7, moves.step_right)
                cfg.handle_button_state('bt8', robot.bt8, moves.circles)

        time.sleep_ms(10)
        
if __name__ == "__main__":
    main()