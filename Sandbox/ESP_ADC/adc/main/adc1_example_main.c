/* ADC1 Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include <stdlib.h>

#include "driver/gpio.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"

#include "esp_sleep.h"
#include "esp_log.h"

#include "driver/gpio.h"
#include "driver/timer.h"
#include "driver/adc.h"
#include "esp_adc_cal.h"

#define GPIO_INPUT_IO_0     0
#define GPIO_INPUT_PIN_SEL  1ULL<<GPIO_INPUT_IO_0
#define ESP_INTR_FLAG_DEFAULT 0

#define DEFAULT_VREF    1100        //Use adc2_vref_to_gpio() to obtain a better estimate
#define NO_OF_SAMPLES   1          //Multisampling

#define ADC_TAG "ADC_W/_CLOCK"
#define ADC_TASK_PRIO     3

static esp_adc_cal_characteristics_t *adc_chars;
static const adc_channel_t channel = ADC_CHANNEL_6;     //GPIO34 if ADC1, GPIO14 if ADC2
static const adc_bits_width_t width = ADC_WIDTH_BIT_12;
static const adc_atten_t atten = ADC_ATTEN_DB_11;
static const adc_unit_t unit = ADC_UNIT_1;

// Variables shared between ISR
#define SAMPLES_TO_TAKE 6
#define NUM_OF_SAMPLES 18000
static uint16_t adc_data_array[NUM_OF_SAMPLES];
static uint32_t esp_time_array[NUM_OF_SAMPLES];

static SemaphoreHandle_t timer_started;
static SemaphoreHandle_t trigger_adc;


static void adc_task(void *arg)
{
    const char *TAG = "adc_task";
    // ESP_LOGD(TAG, "Starting Timers");
    vTaskDelay(pdMS_TO_TICKS(1000));

    ESP_LOGD(TAG, "Waiting on pb");
    xSemaphoreGive(timer_started);

    for (int sample = 0; sample < NUM_OF_SAMPLES; sample++)
    // int sample =0;

    // while (1)
    {
        xSemaphoreTake(trigger_adc,portMAX_DELAY);
        esp_time_array[sample] = esp_timer_get_time();

        uint16_t sum = 0;
        for (int i = 0; i < SAMPLES_TO_TAKE; i++)
            sum += adc1_get_raw(channel);

        adc_data_array[sample] = sum/SAMPLES_TO_TAKE;
        
        // printf("%d\n", adc_data_array[sample]);
        // printf("%d\n", adc1_get_raw((adc1_channel_t)channel));
        // printf("%d,%d.", adc_data_array[sample], esp_time_array[sample] & 0xFFF);
        // sample++;
        if (sample % 20000 == 0){
            vTaskDelay(1);
            // count = 0;
        }


    }


    int sum = 0;
    for (int i = 0; i < NUM_OF_SAMPLES - 1; i++)
    {
        printf("%d,%d,", adc_data_array[i], esp_time_array[i]);
        sum += esp_time_array[i + 1] - esp_time_array[i];

        if (i % 2000 == 0){
            vTaskDelay(1);
           
        }
 
    }
    ESP_LOGD(TAG, "\nAverage Sample Rate %d", (int)(sum / (1.0 * NUM_OF_SAMPLES)));

    while (1)
        vTaskDelay(pdMS_TO_TICKS(100));

    
}


static void IRAM_ATTR gpio_isr_handler(void* arg)
{
    gpio_isr_handler_remove(GPIO_INPUT_IO_0);
    timer_start(TIMER_GROUP_1, TIMER_1);
    // printf("break");
}

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

    const char *TAG = "app_main";

    //Configure ADC----------------------------------------------
    adc1_config_width(width);
    adc1_config_channel_atten(channel, atten);
    
    //Characterize ADC
    adc_chars = calloc(1, sizeof(esp_adc_cal_characteristics_t));
    esp_adc_cal_characterize(unit, atten, width, DEFAULT_VREF, adc_chars);
    // esp_adc_cal_value_t val_type = esp_adc_cal_characterize(unit, atten, width, DEFAULT_VREF, adc_chars);
    // print_char_val_type(val_type);

    //Semaphore Configuration ---------------------------------
    trigger_adc = xSemaphoreCreateBinary();
    timer_started = xSemaphoreCreateBinary();


    //GPIO Init ----------------------------------------------
    gpio_config_t io_conf = {};
    //interrupt of rising edge
    io_conf.intr_type = GPIO_INTR_NEGEDGE;
    //bit mask of the pins, use GPIO4/5 here
    io_conf.pin_bit_mask = GPIO_INPUT_PIN_SEL;
    //set as input mode
    io_conf.mode = GPIO_MODE_INPUT;
    //enable pull-up mode
    io_conf.pull_up_en = 1;
    io_conf.pull_down_en = 0;
    gpio_config(&io_conf);


    //install gpio isr service
    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    //hook isr handler for specific gpio pin
    gpio_isr_handler_add(GPIO_INPUT_IO_0, gpio_isr_handler, (void*) GPIO_INPUT_IO_0);



    //Timer Configuration ---------------------------------
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

    ESP_LOGD(TAG, "Starting freeRTOS Tasks");
    xTaskCreatePinnedToCore(adc_task, "adc", 65536, NULL, ADC_TASK_PRIO, NULL, tskNO_AFFINITY);

    xSemaphoreTake(timer_started, portMAX_DELAY);
    
    // ESP_LOGD(TAG, "Timers Started");

    vTaskDelay(pdMS_TO_TICKS(2000));
}
