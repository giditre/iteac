#include <stdio.h>
#include <wiringPi.h>
#include <wiringShift.h>

#define	GPIOREGD 0
#define GPIOREGST 2
#define GPIOREGSH 3

#define NROWS 8
#define NCOLUMNS 8

void gpio_setup (void) {
  wiringPiSetup();
  // set output mode
  pinMode(GPIOREGD, OUTPUT); 
  pinMode(GPIOREGST, OUTPUT);
  pinMode(GPIOREGSH, OUTPUT);
  // initialize pins
  digitalWrite(GPIOREGD, LOW);
  digitalWrite(GPIOREGST, LOW);
  digitalWrite(GPIOREGSH, LOW);
}

void shift_out_byte (char b) {
  shiftOut(GPIOREGD, GPIOREGSH, MSBFIRST, b);
}

void shift_out_word (uint16_t w) {
  shift_out_byte( w >> 8 );
  shift_out_byte( w & 0x00ff );
}

void store (void) {
  digitalWrite(GPIOREGST, HIGH);
  digitalWrite(GPIOREGST, LOW);
}

void clear (void) {
  shift_out_word((uint16_t) 0);
  store();
}

void light_word(uint16_t w, uint8_t persist) {
  shift_out_word(w);
  store();
  delay(persist);
}

void light_matrix(uint16_t rows[], int duration) {
  float persistence_time = 1;
  int n_cycles = duration / ( NROWS * persistence_time/1000 );
  for (int t=0; t < n_cycles; t++) {
    for (int i=0; i < NROWS; i++) {
      light_word(rows[i], (int) persistence_time);
    }
  }
}

/*
int display_digits(int digits[], int n_digits, int duration) {
  printf ("RasPi iteac 7seg display digits\n");
  // board-related parameters
  float persistence_time = 1;  // time each 7seg display stays on, in milliseconds
  // define index variables
  int i, l;
  // check parameters
  if (n_digits > 8) {
    printf("Too many digits, maximum is 8.\n");
    return 1;
  }
  for (i = 0; i < n_digits; i++) {
    if (digits[i] < 0 || digits[i] > 9) {
      printf("Invalid digits, only 0-9.\n");
      return 2;
    }
  }
  // convert digits to segments and print information
  char segments[8];
  printf("n_digits: %d\n", n_digits);
  for (i = 0; i < n_digits; i++) {
    segments[i] = dispNum[digits[i]];
    printf("digits[%d]: %d -> %d\n", i, digits[i], segments[i]);
  }
  // compute number of cycles to reach desired duration (approx.)
  int n_cycles = duration / ( n_digits * persistence_time/1000 );
  printf("n_cycles: %d\n", n_cycles);
  // setup gpio
  gpio_setup();
  // display digits by cycling over all digits a sufficient number of times to achieve duration
  for (l = 0; l < n_cycles; l++) {
    for (i = 0; i < n_digits; i++) {
      shift_out_byte(segments[i]);
      store();
      set_addr(i);
      delay(persistence_time);
    }
  }
  // clear output and leave
  clear();
  return 0; 
}
*/
