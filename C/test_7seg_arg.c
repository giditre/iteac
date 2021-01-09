#include <stdio.h>
#include <string.h>
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
#define LA SEGa|SEGb|SEGc|SEGe|SEGf|SEGg
#define LB SEGc|SEGd|SEGe|SEGf|SEGg
#define LC SEGa|SEGd|SEGe|SEGf
#define LD SEGb|SEGc|SEGd|SEGe|SEGg
#define LE SEGa|SEGd|SEGe|SEGf|SEGg
#define LF SEGa|SEGe|SEGf|SEGg
#define LG SEGa|SEGc|SEGd|SEGe|SEGf
#define LH SEGb|SEGc|SEGe|SEGf|SEGg
#define LI SEGe|SEGf
#define LJ SEGb|SEGc|SEGd|SEGe
#define LK SEGBLANK // not possible
#define LL SEGd|SEGe|SEGf
#define LM SEGBLANK // not possible
#define LN SEGc|SEGe|SEGg
#define LO SEGa|SEGb|SEGc|SEGd|SEGe|SEGf
#define LP SEGa|SEGb|SEGe|SEGf|SEGg
#define LQ SEGa|SEGb|SEGc|SEGf|SEGg
#define LR SEGe|SEGg
#define LS SEGa|SEGc|SEGd|SEGf|SEGg
#define LT SEGd|SEGe|SEGf|SEGg
#define LU SEGb|SEGc|SEGd|SEGe|SEGf
#define LV SEGBLANK // not possible
#define LW SEGBLANK // not possible
#define LX SEGBLANK // not possible
#define LY SEGb|SEGc|SEGd|SEGf|SEGg
#define LZ SEGa|SEGb|SEGd|SEGe|SEGg
#define LSPACE SEGBLANK

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

int main (int argc, char** argv) {

  printf ("RasPi iteac 7seg test with %d arguments\n", argc);

  if (argc > 8+1+1) {
    printf("Too many arguments!\n");
    printf("Usage: %s <duration> <digit> [<digit> ... ]\n", argv[0]);
    return 1;
  }

  // parse duration arg
  int duration;
  sscanf(argv[1], "%d", &duration);

  // parse digits args in an array of values of dispNum

  char digits[8];
  int n_digits = 0;
  int i, l, n;

  for (i = 2; i < argc; i++) {
    sscanf(argv[i], "%d", &n);
    digits[i-2] = dispNum[n];
    printf("argv[%d]: %s -> dispNum[%d]: %x -> digits[%d]: %x\n", i, argv[i], n, dispNum[n], i-2, digits[i-2]);
    n_digits++;
  }
  printf("n_digits: %d\n", n_digits);

  // setup gpio pins

  gpio_setup();
  
  // display digits

  int n_cycles = duration * 1000 / n_digits;
  printf("n_cycles: %d\n", n_cycles);

  for (l = 0; l < n_cycles; l++) {
    for (i = 0; i < n_digits; i++) {
      shiftOut(GPIOREGD, GPIOREGSH, MSBFIRST, digits[i]);
      store();
      set_addr(i);
      delay(1);
    }
  }

  // clear output
  
  clear();

  return 0;
}
