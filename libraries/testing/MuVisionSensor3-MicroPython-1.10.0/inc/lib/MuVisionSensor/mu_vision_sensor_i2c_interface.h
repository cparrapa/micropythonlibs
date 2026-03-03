// Copyright 2018 Morpx Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef ARDUINO_LIB_MUVISIONSENSOR_SRC_MU_VISION_SENSOR_I2C_INTERFACE_H_
#define ARDUINO_LIB_MUVISIONSENSOR_SRC_MU_VISION_SENSOR_I2C_INTERFACE_H_

#include "mu_vision_sensor_interface.h"

//Error Type
#define MU_OK                         0x00
#define MU_FAIL                       0x01
#define MU_WRITE_TIMEOUT              0x02
#define MU_READ_TIMEOUT               0x03
#define MU_CHECK_ERROR                0x04
#define MU_UNKNOW_PARAM               0x10
#define MU_UNKNOW_PROTOCOL            0x11
#define MU_SLAVE_OK                   0xE0
#define MU_SLAVE_FAIL                 0xE1
#define MU_SLAVE_UNKNOW               0xE2
#define MU_SLAVE_TIMEOUT              0xE3
#define MU_SLAVE_CHECK_ERROR          0xE4
#define MU_SLAVE_LENGTH_ERROR         0xE5
#define MU_SLAVE_UNKNOW_COMMAND       0xE6
#define MU_SLAVE_UNKNOW_REG_ADDRESS   0xE7
#define MU_SLAVE_UNKNOW_REG_VALUE     0xE8
#define MU_SLAVE_READ_ONLY            0xE9
#define MU_SLAVE_RESTART_ERROR        0xEA

class MuVsI2CMethod : public MuVsMethod {
 public:
  MuVsI2CMethod(uint32_t address);
  virtual ~MuVsI2CMethod(void);
  MuVsI2CMethod(const MuVsI2CMethod&) = delete;
  MuVsI2CMethod& operator=(const MuVsI2CMethod &) = delete;

  virtual uint32_t I2CRead(uint8_t reg_address, uint8_t* temp) = 0;
  virtual uint32_t I2CWrite(uint8_t reg_address, uint8_t value) = 0;

  virtual mu_err_t Get(const uint8_t reg_address,
                       uint8_t* value) override;
  virtual mu_err_t Set(const uint8_t reg_address,
                       const uint8_t value) override;
  mu_err_t Read(MuVsMessageVisionType vision_type,
                MuVsVisionState* vision_state);

 private:

 protected:
};

#endif /* ARDUINO_LIB_MUVISIONSENSOR_SRC_MU_VISION_SENSOR_UART_INTERFACE_H_ */
