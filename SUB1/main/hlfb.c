
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "esp_log.h"

#include "driver/gpio.h"

#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/task.h"

#include "message_handling.c"

// Set the freq of the High Level Feed Back
#define MODE_45Hz 45
#define MODE_482Hz 482
#define HLFB_FREQ MODE_45Hz
#define ESP_INTR_FLAG_DEFAULT 0

#define GPIO_MOTOR_HLFB 32
#define GPIO_INPUT_PINS_SEL (1ULL << GPIO_MOTOR_HLFB)

static uint32_t hlfb_rising = 0;
static uint32_t hlfb_falling = 0;

static SemaphoreHandle_t hlfb_rising_edge_detected;

// Interrupt handler for gpio event
static void IRAM_ATTR hlfb_isr_handler(void *arg)
{
    // Check if rising or falling
    if (gpio_get_level(GPIO_MOTOR_HLFB))
    {
        // Get time and Awake duty_cycle_calculator
        hlfb_rising = esp_timer_get_time();
        BaseType_t xHigherPriorityTaskWoken = pdTRUE;
        xSemaphoreGiveFromISR(hlfb_rising_edge_detected, &xHigherPriorityTaskWoken);
    }
    else
        // Get time of rise
        hlfb_falling = esp_timer_get_time();
}

/*
This function configures the gpio input for hlfb from clearpath motor
*/
static void configure_gpio_input()
{

    gpio_config_t io_conf = {};
    ESP_LOGI("HLFB", "GPIO Input Init");
    io_conf.intr_type = GPIO_INTR_ANYEDGE;
    io_conf.pin_bit_mask = GPIO_INPUT_PINS_SEL;
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pull_up_en = 1;
    gpio_config(&io_conf);

    // Enable Intr for hlfb
    gpio_set_intr_type(GPIO_MOTOR_HLFB, GPIO_INTR_ANYEDGE);
    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    gpio_isr_handler_add(GPIO_MOTOR_HLFB, hlfb_isr_handler, (void *)GPIO_INPUT_PINS_SEL);
    gpio_intr_enable(GPIO_MOTOR_HLFB);
}

// Function to collect motor torque and send to python program
static void duty_cycle_calculator_task(void *arg)
{
    ESP_LOGI("HLFB", "Creating Semaphore");
    hlfb_rising_edge_detected = xSemaphoreCreateBinary();

    configure_gpio_input();

    int sample_count = 0;
    int samles_to_collect = 5;
    int avg = 0;
    for (;;)
    {
        // Wait for rising edge
        xSemaphoreTake(hlfb_rising_edge_detected, portMAX_DELAY);

        // Add length of 0 logic to the average
        avg += (hlfb_rising - hlfb_falling);
        sample_count++;

        // Check if reached max samples to collect
        if (sample_count >= samles_to_collect)
        {
            // Send torque reading to subsystem3
            printf("TOR:%f\n", (avg / samles_to_collect / (1.0 / HLFB_FREQ)) / 1000000.);
            avg = 0;
            sample_count = 0;
        }
    }
}
