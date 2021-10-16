
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


#define GPIO_INPUT_FROM_MOTOR     (1ULL<<5)

static uint32_t hlfb_rising = 0;
static uint32_t hlfb_falling = 0;


static SemaphoreHandle_t hlfb_rising_edge_detected;

 static void IRAM_ATTR hlfb_isr_handler(void *arg)
 {
    //  uint32_t gpio_num = (uint32_t) arg;
    // hlfb_falling = gpio_get_level(GPIO_NUM_5);
    
    if (gpio_get_level(GPIO_NUM_5))
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
    printf("We are here!!");
    int count = 0;
    int  max = 15;
    int avg = 0;
    for (;;)
    {
        count++;
        xSemaphoreTake(hlfb_rising_edge_detected, portMAX_DELAY);
        avg += (hlfb_rising - hlfb_falling);
        // float duty_cycle = ((hlfb_rising - hlfb_falling));// / (1.0 / HLFB_FREQ))/ 1000000.;
        if (count >= max)
        {

            printf("HLFB: MOTOR: Duty Cycle %f\n", (avg/max/ (1.0 / HLFB_FREQ))/ 1000000.);
            avg = 0;
            count = 0;
        }
        // printf("%d\n", hlfb_falling);
    }
}

void app_main(void)
{
    printf("Starting app_main");

    hlfb_rising_edge_detected = xSemaphoreCreateBinary();


    //zero-initialize the config structure.
    gpio_config_t io_conf = {};
    //disable interrupt
    io_conf.intr_type = GPIO_INTR_DISABLE;
    //set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    //bit mask of the pins that you want to set,e.g.GPIO18/19
    io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL;
    //disable pull-down mode
    io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 0;
    //configure GPIO with the given settings
    gpio_config(&io_conf);

    //interrupt of rising edge
    io_conf.intr_type = GPIO_INTR_ANYEDGE;
    //bit mask of the pins
    io_conf.pin_bit_mask = GPIO_INPUT_FROM_MOTOR;
    //set as input mode
    io_conf.mode = GPIO_MODE_INPUT;
    //enable pull-up mode
    io_conf.pull_down_en = 1;
    gpio_config(&io_conf);

    
    printf("Starting Task");
    //start gpio task
    xTaskCreate(duty_cycle_calculator_task, "duty_cycle_calculator", 2048, NULL, 5, NULL);

    gpio_set_intr_type(5, GPIO_INTR_ANYEDGE);
    //install gpio isr service
    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    gpio_isr_handler_add(5, hlfb_isr_handler, (void*) GPIO_INPUT_FROM_MOTOR);

    gpio_intr_enable(GPIO_INPUT_FROM_MOTOR);
    

}
