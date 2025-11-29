#include "vectorclass.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <assert.h>
#include <math.h>

// baseline implementation of dot product
double dot_product_baseline(double* arr1, double* arr2, uint64_t length){
    double sum = 0.0;
    for(uint64_t i = 0; i < length; i++){
        sum += arr1[i]*arr2[i];
    }
    return sum;
}

// independent instruction implementation of dot product
double dot_product_independent(double* arr1, double* arr2, uint64_t length){
    double sum0 = 0.0;
    double sum1 = 0.0;
    double sum2 = 0.0;
    double sum3 = 0.0;
    uint64_t i = 0;
    for(; i+3 < length; i+=4){
        sum0 += arr1[i]*arr2[i];
        sum1 += arr1[i+1]*arr2[i+1];
        sum2 += arr1[i+2]*arr2[i+2];
        sum3 += arr1[i+3]*arr2[i+3];
    }
    double sum = sum0+sum1+sum2+sum3;
    for(; i < length; i++){
        sum += arr1[i]*arr2[i];
    }
    return sum;
}

// SIMD instruction implementation of dot product
double dot_product_SIMD(double* arr1, double* arr2, uint64_t length){
    Vec4d sum = 0.0;
    uint64_t i = 0;
    for(; i+3 < length; i+=4){
        Vec4d vec1;
        vec1.load(arr1+i);
        Vec4d vec2;
        vec2.load(arr2+i);
        sum += vec1*vec2;
    }
    double result = horizontal_add(sum);
    for(; i < length; i++){
        result += arr1[i]*arr2[i];
    }
    return result;
}

// create a random double array
double* create_array(uint64_t length) {
    double* array = (double*)malloc(length * sizeof(double));
    if (array == NULL) {
        return NULL;
    }
    for (uint64_t i = 0; i < length; i++) {
        array[i] = ((double)rand() / RAND_MAX - 0.25);
    }
    return array;
}



// main function
int main(void){
    uint64_t length = 25000; //25000 -> small data 200000000 -> large data
    double* arr1 = create_array(length);
    double* arr2 = create_array(length);
    assert(arr1 != NULL);
    assert(arr2 != NULL);
    struct timespec start, end;
    double elapsed;
    double result = 0.0;
    // for large data
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    result = dot_product_baseline(arr1,arr2,length);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    elapsed = (end.tv_sec-start.tv_sec)+(end.tv_nsec-start.tv_nsec)/1e9;
    printf("Baseline: %.4f ms (Result: %f)\n", elapsed*1000,result);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    result = dot_product_independent(arr1,arr2,length);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    elapsed = (end.tv_sec-start.tv_sec)+(end.tv_nsec-start.tv_nsec)/1e9;
    printf("Independent: %.4f ms (Result: %f)\n", elapsed*1000,result);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    result = dot_product_SIMD(arr1,arr2,length);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    elapsed = (end.tv_sec-start.tv_sec)+(end.tv_nsec-start.tv_nsec)/1e9;
    printf("SIMD: %.4f ms (Result: %f)\n", elapsed*1000,result);
    //for small data
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    for(int i = 0; i < 100000; i++){
        result += dot_product_baseline(arr1,arr2,length);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    elapsed = (end.tv_sec-start.tv_sec)+(end.tv_nsec-start.tv_nsec)/1e9;
    printf("Baseline: %.4f ms (Result: %f)\n", elapsed*1000,result);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    for(int i = 0; i < 100000; i++){
        result += dot_product_independent(arr1,arr2,length);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    elapsed = (end.tv_sec-start.tv_sec)+(end.tv_nsec-start.tv_nsec)/1e9;
    printf("Independent: %.4f ms (Result: %f)\n", elapsed*1000,result);
    
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    for(int i = 0; i < 100000; i++){
        result += dot_product_SIMD(arr1,arr2,length);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    elapsed = (end.tv_sec-start.tv_sec)+(end.tv_nsec-start.tv_nsec)/1e9;
    printf("SIMD: %.4f ms (Result: %f)\n", elapsed*1000,result);
    return 0;
}