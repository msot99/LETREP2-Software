
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/gpio.h"


 // Set the freq of the High Level Feed Back
#define MODE_45Hz  45
#define MODE_482Hz  482
#define HLFB_FREQ MODE_45Hz

#define ESP_INTR_FLAG_DEFAULT 0

#define GPIO_OUTPUT_ENABLE_PIN    18
#define GPIO_OUTPUT_FIRE_PIN      19
#define GPIO_OUTPUT_PIN_SEL  ((1ULL<<GPIO_OUTPUT_ENABLE_PIN) | (1ULL<<GPIO_OUTPUT_FIRE_PIN))


#define GPIO_INPUT_FROM_MOTOR     5

static uint32_t hlfb_rising = 0;
static uint32_t hlfb_falling = 0;


static SemaphoreHandle_t hlfb_rising_edge_detected;

 static void IRAM_ATTR hlfb_isr_handler(void *arg)
 {
     if (gpio_get_level((uint32_t)arg))
     {
        hlfb_rising = esp_timer_get_time();
        BaseType_t xHigherPriorityTaskWoken = pdTRUE;
        xSemaphoreGiveFromISR(hlfb_rising_edge_detected, &xHigherPriorityTaskWoken );

     }
     else
         hlfb_falling = esp_timer_get_time();
 }


static void duty_cycle_calculator_task(void* arg)
{
    
    for(;;) {
        xSemaphoreTake(hlfb_rising_edge_detected,portMAX_DELAY);
        float duty_cycle = ((hlfb_rising - hlfb_falling) / (1.0 / HLFB_FREQ))/ 10000000.;
        printf("HLFB: MOTOR: Duty Cycle %f", duty_cycle);
    }
}

void app_main(void)
{
    
    hlfb_rising_edge_detected = xSemaphoreCreateBinary();


    // //zero-initialize the config structure.
    gpio_config_t io_conf = {};
    // //disable interrupt
    // io_conf.intr_type = GPIO_INTR_DISABLE;
    // //set as output mode
    // io_conf.mode = GPIO_MODE_OUTPUT;
    // //bit mask of the pins that you want to set,e.g.GPIO18/19
    // io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL;
    // //disable pull-down mode
    // io_conf.pull_down_en = 0;
    // //disable pull-up mode
    // io_conf.pull_up_en = 0;
    // //configure GPIO with the given settings
    // gpio_config(&io_conf);

    //interrupt of rising edge
    io_conf.intr_type = GPIO_INTR_POSEDGE;
    //bit mask of the pins
    io_conf.pin_bit_mask = GPIO_INPUT_FROM_MOTOR;
    //set as input mode
    io_conf.mode = GPIO_MODE_INPUT;
    //enable pull-up mode
    io_conf.pull_down_en = 1;
    gpio_config(&io_conf);


    //start gpio task
    xTaskCreate(duty_cycle_calculator_task, "duty_cycle_calculator", 1024, NULL, 5, NULL);

    //install gpio isr service
    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    gpio_isr_handler_add(GPIO_INPUT_FROM_MOTOR, hlfb_isr_handler, (void*) GPIO_INPUT_FROM_MOTOR);



}
