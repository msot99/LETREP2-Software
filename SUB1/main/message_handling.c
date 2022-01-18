
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "esp_log.h"

#include "driver/gpio.h"

#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/task.h"

#include "driver/uart.h"

#define GPIO_MOTOR_ENABLE 25
#define GPIO_MOTOR_A 26
#define GPIO_MOTOR_B 33
#define GPIO_OUTPUT_PINS_SEL ((1ULL << GPIO_MOTOR_ENABLE) | (1ULL << GPIO_MOTOR_A) | (1ULL << GPIO_MOTOR_B))

#define BUF_SIZE (1024)

#define UART_PORT_NUM UART_NUM_0

static SemaphoreHandle_t uart_mutex;

/*
This function configures the gpio output for motor control
*/
static void configure_gpio_output()
{
    // Set initial value to 1

    ESP_LOGI("message_handling", "Setting GPIO Output");

    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = GPIO_OUTPUT_PINS_SEL;
    io_conf.pull_down_en = 0;
    io_conf.pull_up_en = 0;
    gpio_config(&io_conf);

    gpio_set_level(GPIO_MOTOR_A, 1);
}

/*
This is a freertos task that processes messages from subsystem3 and converts to motor controls.
*/
static void command_processor_task(void *arg)
{

    ESP_LOGI("COMMAND_PROCESSOR_TASK", "Creating Semaphores");
    uart_mutex = xSemaphoreCreateMutex();
    configure_gpio_output();

    ESP_ERROR_CHECK(uart_driver_install(UART_PORT_NUM, BUF_SIZE * 2, 0, 0, NULL, 0));

    uint8_t *data = (uint8_t *)malloc(BUF_SIZE);
    // uint8_t data = 0;
    while (1)
    {
        uart_read_bytes(UART_PORT_NUM, data, BUF_SIZE, 20 / portTICK_RATE_MS);

        xSemaphoreTake(uart_mutex, portMAX_DELAY);
        switch (*data)
        {
        case 97:

            gpio_set_level(GPIO_MOTOR_ENABLE, 1);
            ESP_LOGI("COMMAND_PROCESSOR_TASK", "Received a");
            printf("enabled\n");
            break;

        case 98:

            gpio_set_level(GPIO_MOTOR_A, 1);
            ESP_LOGI("COMMAND_PROCESSOR_TASK", "Received b");
            printf("ack\n");
            break;
        case 99:

            gpio_set_level(GPIO_MOTOR_A, 0);
            ESP_LOGI("COMMAND_PROCESSOR_TASK", "Received c");
            printf("ack\n");
            break;
        case 100:

            gpio_set_level(GPIO_MOTOR_ENABLE, 0);
            ESP_LOGI("COMMAND_PROCESSOR_TASK", "Received d");
            printf("disabled\n");
            break;
        default:
            break;
        }
        *data = 0;
        xSemaphoreGive(uart_mutex);
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}
