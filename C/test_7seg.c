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
  digitalWrite (GPIOADDR0, (addr[a]>>2)&1) ;
  digitalWrite (GPIOADDR1, (addr[a]>>1)&1) ;
  digitalWrite (GPIOADDR2, (addr[a]>>0)&1) ;
}

void store (void) {
  digitalWrite (GPIOREGST, HIGH) ;
  //delay (500) ;   // mS 
  digitalWrite (GPIOREGST, LOW) ;
  //delay (500) ;
}

void clear (void) {
  set_addr(0) ;
  shiftOut (GPIOREGD, GPIOREGSH, MSBFIRST, 0) ;
  store () ;
}

int main (void) {

  printf ("RasPi iteac 7seg test\n") ;

  wiringPiSetup () ;
 
  pinMode (GPIOREGD, OUTPUT) ; 
  pinMode (GPIOREGST, OUTPUT) ;
  pinMode (GPIOREGSH, OUTPUT) ;
  pinMode (GPIOADDR0, OUTPUT) ;
  pinMode (GPIOADDR1, OUTPUT) ;
  pinMode (GPIOADDR2, OUTPUT) ;

  digitalWrite (GPIOREGD, LOW) ;
  digitalWrite (GPIOREGST, LOW) ;
  digitalWrite (GPIOREGSH, LOW) ;
  digitalWrite (GPIOADDR0, LOW) ;
  digitalWrite (GPIOADDR1, LOW) ;
  digitalWrite (GPIOADDR2, LOW) ;

  for (int a=0; a<=7; a++) {
    set_addr(a) ;
    for (int i=0 ; i<=9 ; i++) {
      shiftOut (GPIOREGD, GPIOREGSH, MSBFIRST, dispNum[i]) ;
      store () ;
      delay (100) ;   // mS
    }
  }

  for (uint16_t i=0; i<1000; i++) {
    for (int a=0; a<=7; a++) {
      set_addr(a) ;
      delay(1) ;
      //delayMicroseconds (10) ;
      shiftOut (GPIOREGD, GPIOREGSH, MSBFIRST, dispNum[a]) ;
      store () ;
    }
    //delay(10) ;
  }

  clear() ;

  return 0 ;
}
