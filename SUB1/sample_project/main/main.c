
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "esp_log.h"

#include "driver/gpio.h"

#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/task.h"
#include "freertos/queue.h"

 // Set the freq of the High Level Feed Back
#define MODE_45Hz  45
#define MODE_482Hz  482
#define HLFB_FREQ MODE_45Hz
#define ESP_INTR_FLAG_DEFAULT 0


#define MOTOR_CAL_TIMEOUT    5
#define MOTOR_CAL_TOR_AMT   .51

#define GPIO_MOTOR_ENABLE    21
#define GPIO_MOTOR_A         18
#define GPIO_MOTOR_B         19
#define GPIO_OUTPUT_PINS_SEL  ((1ULL<<GPIO_MOTOR_ENABLE) | (1ULL<<GPIO_MOTOR_A) | (1ULL<<GPIO_MOTOR_B) )

#define GPIO_MOTOR_HLFB     5
#define GPIO_INPUT_PINS_SEL  (1ULL<<GPIO_MOTOR_HLFB)

static uint32_t hlfb_rising = 0;
static uint32_t hlfb_falling = 0;
static uint32_t torque_duty_cycle;

static SemaphoreHandle_t uart_mutex;
static SemaphoreHandle_t hlfb_rising_edge_detected;

 static void IRAM_ATTR hlfb_isr_handler(void *arg)
 {
     // Check if rising or falling
    if (gpio_get_level(GPIO_MOTOR_HLFB))
    {   
        // Get time and Awake duty_cycle_calculator
        hlfb_rising = esp_timer_get_time();
        BaseType_t xHigherPriorityTaskWoken = pdTRUE;
        xSemaphoreGiveFromISR(hlfb_rising_edge_detected, &xHigherPriorityTaskWoken );
     }
     else
        // Get time of rise
        hlfb_falling = esp_timer_get_time();
 }

// Function to collect motor torque and send to python program
static void duty_cycle_calculator_task(void* arg)
{
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
            torque_duty_cycle = (avg / samles_to_collect / (1.0 / HLFB_FREQ)) / 1000000.;
            xSemaphoreTake(uart_mutex, portMAX_DELAY);
            printf("101:%f\n", (avg/samles_to_collect/ (1.0 / HLFB_FREQ))/ 1000000.);
            xSemaphoreGive(uart_mutex);
            avg = 0;
            sample_count = 0;
        }
    }
}

/* When motor starts, the postition of the peddle/ pully system is unknown.
Calibration process:
    1. Enable motor (This initilizes homing, motor spends until B is triggered)
    2. Wait for motor to reach endstop and torque to increase
    3. Set Motor Input B High
*/
static void set_motor_position()
{
    ESP_LOGI("set_motor_position", "Starting Motor Pos Calibration");
    // Enable Motor
    gpio_set_level(GPIO_MOTOR_ENABLE, 1);

    uint32_t enable_time = esp_timer_get_time();
    while(1)
    {
        if (esp_timer_get_time()-enable_time>(MOTOR_CAL_TIMEOUT * 1000000))
        {
            ESP_LOGE("set_motor_position", "Motor Cal Timeout Error!!!!!");
            vTaskEndScheduler();
            while(1)
                ;
        }
        if (torque_duty_cycle > MOTOR_CAL_TOR_AMT)
        {
            gpio_set_level(GPIO_MOTOR_B, 1);
            ESP_LOGI("set_motor_position", "Motor Calibration Set");
        }
        vTaskDelay(pdMS_TO_TICKS(200));
    }



}


void app_main(void)
{
    ESP_LOGI("APP_MAIN", "Starting");


    ESP_LOGI("APP_MAIN", "Creating Semaphores");
    hlfb_rising_edge_detected = xSemaphoreCreateBinary();
    uart_mutex = xSemaphoreCreateMutex();


    ESP_LOGI("APP_MAIN", "GPIO Output Init");
    //zero-initialize the config structure.
    gpio_config_t io_conf = {};
    //disable interrupt
    io_conf.intr_type = GPIO_INTR_DISABLE;
    //set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    //bit mask of the pins that you want to set,e.g.GPIO18/19/21
    io_conf.pin_bit_mask = GPIO_OUTPUT_PINS_SEL;
    //disable pull-down mode
    io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 0;
    //configure GPIO with the given settings
    gpio_config(&io_conf);

    ESP_LOGI("APP_MAIN", "GPIO Input Init");
    //interrupt of rising edge
    io_conf.intr_type = GPIO_INTR_ANYEDGE;
    //bit mask of the pins
    io_conf.pin_bit_mask = GPIO_INPUT_PINS_SEL;
    //set as input mode
    io_conf.mode = GPIO_MODE_INPUT;
    //enable pull-up mode
    io_conf.pull_down_en = 1;
    gpio_config(&io_conf);

    
    ESP_LOGI("APP_MAIN", "FreeRTOS Tasks Starting");
    //Starting FreeRTOS tasks
    xTaskCreate(duty_cycle_calculator_task, "duty_cycle_calculator", 2048, NULL, 5, NULL);


    
    gpio_set_intr_type(GPIO_MOTOR_HLFB, GPIO_INTR_ANYEDGE);
    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    gpio_isr_handler_add(GPIO_MOTOR_HLFB, hlfb_isr_handler, (void*) GPIO_INPUT_PINS_SEL);
    gpio_intr_enable(GPIO_MOTOR_HLFB);
    

}
