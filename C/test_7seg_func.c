#include <stdio.h>
#include <wiringPi.h>
#include <wiringShift.h>

#define	GPIOREGD 4
#define GPIOREGST 5
#define GPIOREGSH 6
#define GPIOADDR0 10
#define GPIOADDR1 11
#define GPIOADDR2 26

#define dispType 0 // only 2 possible values: 0 for common cathode or 255 for common anode

/*
Diagram of segments on a 7seg display
   A
 |---|
F| G |B
  ---
E|   |C
 |---|
   D  .P
*/

// segment to reg position mapping
#define SEGa 0b00000010
#define SEGb 0b00000001
#define SEGc 0b00001000
#define SEGd 0b00100000
#define SEGe 0b00010000
#define SEGf 0b10000000
#define SEGg 0b01000000
#define SEGp 0b00000100
#define SEGBLANK 0b00000000

#define N0 SEGa|SEGb|SEGc|SEGd|SEGe|SEGf
#define N1 SEGb|SEGc
#define N2 SEGa|SEGb|SEGd|SEGe|SEGg
#define N3 SEGa|SEGb|SEGc|SEGd|SEGg
#define N4 SEGb|SEGc|SEGf|SEGg
#define N5 SEGa|SEGc|SEGd|SEGf|SEGg
#define N6 SEGa|SEGc|SEGd|SEGe|SEGf|SEGg
#define N7 SEGa|SEGb|SEGc
#define N8 SEGa|SEGb|SEGc|SEGd|SEGe|SEGf|SEGg
#define N9 SEGa|SEGb|SEGc|SEGd|SEGf|SEGg

const unsigned char dispNum[]={N0,N1,N2,N3,N4,N5,N6,N7,N8,N9};

const unsigned char addr[]={6,2,4,0,7,3,5,1};

void set_addr (int a) {
  digitalWrite (GPIOADDR0, (addr[a]>>2)&1);
  digitalWrite (GPIOADDR1, (addr[a]>>1)&1);
  digitalWrite (GPIOADDR2, (addr[a]>>0)&1);
}

void store (void) {
  digitalWrite (GPIOREGST, HIGH);
  //delay (500);   // mS 
  digitalWrite (GPIOREGST, LOW);
  //delay (500);
}

void clear (void) {
  set_addr(0);
  shiftOut(GPIOREGD, GPIOREGSH, MSBFIRST, 0);
  store();
}

void gpio_setup (void) {
  wiringPiSetup();
 
  pinMode(GPIOREGD, OUTPUT); 
  pinMode(GPIOREGST, OUTPUT);
  pinMode(GPIOREGSH, OUTPUT);
  pinMode(GPIOADDR0, OUTPUT);
  pinMode(GPIOADDR1, OUTPUT);
  pinMode(GPIOADDR2, OUTPUT);

  digitalWrite(GPIOREGD, LOW);
  digitalWrite(GPIOREGST, LOW);
  digitalWrite(GPIOREGSH, LOW);
  digitalWrite(GPIOADDR0, LOW);
  digitalWrite(GPIOADDR1, LOW);
  digitalWrite(GPIOADDR2, LOW);

}

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
      shiftOut(GPIOREGD, GPIOREGSH, MSBFIRST, segments[i]);
      store();
      set_addr(i);
      delay(persistence_time);
    }
  }
  // clear aoutput and leave
  clear();
  return 0; 
}

