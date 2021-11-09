
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "esp_log.h"

#include "driver/gpio.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "hlfb.c"

void app_main(void)
{
    ESP_LOGI("APP_MAIN", "FreeRTOS Tasks Starting");

    //Starting FreeRTOS tasks
    xTaskCreate(command_processor_task, "command_processor_task", 4096, NULL, 4, NULL);
    xTaskCreate(duty_cycle_calculator_task, "duty_cycle_calculator", 2048, NULL, 5, NULL);
}
