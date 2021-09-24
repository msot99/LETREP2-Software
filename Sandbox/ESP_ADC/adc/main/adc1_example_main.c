#include <stdio.h>
#include <stdlib.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"

#include "esp_sleep.h"
#include "esp_log.h"

#include "driver/gpio.h"
#include "driver/timer.h"
#include "driver/adc.h"


#define ADC_TASK_PRIO     3

static const adc_channel_t channel = ADC_CHANNEL_6;
static const adc_bits_width_t width = ADC_WIDTH_BIT_12;
static const adc_atten_t atten = ADC_ATTEN_DB_11;

// Multisampling
#define NO_OF_SAMPLES   6  

static SemaphoreHandle_t timer_started;
static SemaphoreHandle_t trigger_adc;

// freeRTOS Task to take samples and send data
static void adc_task(void *arg)
{
    const char *TAG = "adc_task";


    // Start Timer
    ESP_LOGD(TAG, "Starting Timers");
    timer_start(TIMER_GROUP_1, TIMER_1);
    vTaskDelay(pdMS_TO_TICKS(1000));
    xSemaphoreGive(timer_started);

    ESP_LOGD(TAG, "START");

    while (1)
    {
        // Wait for timer trigger
        xSemaphoreTake(trigger_adc,portMAX_DELAY);

        // Note time of trigger, this is used to determine time between samples
        uint32_t time_triggered = esp_timer_get_time();
        
        // Read Samples, uses multisampling to reduce noise
        uint16_t sum = 0;
        for (int i = 1; i < NO_OF_SAMPLES; i++)
            sum += adc1_get_raw(channel);
   
        // Send Samples average
        printf("%d,%d\n",  sum/NO_OF_SAMPLES, time_triggered);
    }    
}


// ADC Timer Callback
static bool IRAM_ATTR timer_group_isr_callback(void *args)
{
    BaseType_t xHigherPriorityTaskWoken = pdTRUE;
    xSemaphoreGiveFromISR(trigger_adc, &xHigherPriorityTaskWoken );
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
        
    return 1;
}


void app_main(void)
{   
    //Wait for CPU to start
    vTaskDelay(pdMS_TO_TICKS(1000));

    // Tag for Debugging
    const char *TAG = "app_main";

    //Configure ADC----------------------------------------------
    adc1_config_width(width);
    adc1_config_channel_atten(channel, atten);
    
    //Semaphore Configuration ---------------------------------
    trigger_adc = xSemaphoreCreateBinary();
    timer_started = xSemaphoreCreateBinary();

    //Timer for ADC Configuration ---------------------------------
    timer_config_t config = {
        .divider = 80,
        .counter_dir = TIMER_COUNT_UP,
        .counter_en = TIMER_PAUSE,
        .alarm_en = TIMER_ALARM_EN,
        .auto_reload = TIMER_AUTORELOAD_EN,
    }; // default clock source is APB
    
    timer_init(TIMER_GROUP_1, TIMER_1, &config);
    timer_set_counter_value(TIMER_GROUP_1, TIMER_1, 0);
    timer_set_alarm_value(TIMER_GROUP_1, TIMER_1, 333);
    timer_enable_intr(TIMER_GROUP_1, TIMER_1);
    timer_isr_callback_add(TIMER_GROUP_1, TIMER_1, timer_group_isr_callback, NULL, 0);


    // Start tasks
    ESP_LOGD(TAG, "Starting freeRTOS Tasks");
    xTaskCreatePinnedToCore(adc_task, "adc", 65536, NULL, ADC_TASK_PRIO, NULL, tskNO_AFFINITY);


    // Wait for task to start
    xSemaphoreTake(timer_started, portMAX_DELAY);
}
