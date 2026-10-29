/**
 * @file os_semantics.h
 * @brief System API for General Semantic Text Analysis
 * 
 * Данный API предоставляет приложениям доступ к подсистеме распознавания 
 * и семантического анализа текстов на уровне операционной системы
 */

#ifndef OS_SEMANTICS_H
#define OS_SEMANTICS_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    SEM_SUCCESS = 0,
    SEM_ERR_NOT_INITIALIZED = -1,
    SEM_ERR_INVALID_HANDLE  = -2,
    SEM_ERR_DOMAIN_NOT_FOUND = -3,
    SEM_ERR_OUT_OF_MEMORY   = -4,
    SEM_ERR_INTERNAL        = -5
} SemStatus;

/** 
 * @brief Дескриптор (Handle) семантической сессии
 * Скрывает внутреннюю структуру от приложения
 */
typedef void* HSEMANTIC_SESSION;

/** @brief Структура, описывающая найденную в тексте сущность */
typedef struct {
    char* entity_type;   /* Тип сущности */
    char* value;         /* Значение сущности */
    float confidence;    /* Уверенность модели (от 0.0 до 1.0) */
} SemEntity;

/** @brief Главная структура с результатами анализа */
typedef struct {
    char* intent;        /* Классифицированное намерение текста */
    char* summary;       /* Краткая выжимка/суммаризация текста */
    
    SemEntity* entities; /* Массив извлеченных сущностей */
    size_t entity_count; /* Количество сущностей в массиве */
} SemResult;

/**
 * @brief Инициализирует системную службу семантики
 * Вызывается при старте ОС или службы
 */
SemStatus SemSys_Initialize();

/**
 * @brief Останавливает системную службу и выгружает модели из RAM
 */
SemStatus SemSys_Shutdown();

/**
 * @brief Создает сессию для конкретной предметной области
 * 
 * @param domain_name Имя предметной области ("medicine")
 * @param out_handle Указатель, куда будет записан дескриптор сессии
 * @return SemStatus Код результата выполнения
 */
SemStatus SemSys_CreateSession(const char* domain_name, HSEMANTIC_SESSION* out_handle);

/**
 * @brief Выполняет семантический анализ текста
 * 
 * @param handle Дескриптор открытой сессии
 * @param text_utf8 Исходный текст для анализа (UTF-8)
 * @param out_result Указатель на структуру результата
 * @return SemStatus Код результата выполнения.
 */
SemStatus SemSys_AnalyzeText(HSEMANTIC_SESSION handle, const char* text_utf8, SemResult** out_result);

/**
 * @brief Освобождает память, выделенную ОС под результаты анализа
 * Приложение ОБЯЗАНО вызывать эту функцию во избежание утечек памяти
 * 
 * @param result Указатель на структуру результата, которую нужно удалить
 */
void SemSys_FreeResult(SemResult* result);

/**
 * @brief Закрывает сессию и освобождает ресурсы конкретного контекста
 * 
 * @param handle Дескриптор сессии
 * @return SemStatus Код результата
 */
SemStatus SemSys_CloseSession(HSEMANTIC_SESSION handle);

#ifdef __cplusplus
}
#endif

#endif