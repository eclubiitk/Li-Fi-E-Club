#include<stdio.h>

int temp = 8 ;
int encoder(int in) {
  switch(in) {
    case  0 : return 30 ; break ;
    case  1 : return  9 ; break ;
    case  2 : return 20 ; break ;
    case  3 : return 21 ; break ;
    case  4 : return 10 ; break ;
    case  5 : return 11 ; break ;
    case  6 : return 14 ; break ;
    case  7 : return 15 ; break ;
    case  8 : return 18 ; break ;
    case  9 : return 19 ; break ;
    case 10 : return 22 ; break ;
    case 11 : return 23 ; break ;
    case 12 : return 26 ; break ;
    case 13 : return 27 ; break ;
    case 14 : return 28 ; break ;
    case 15 : return 29 ; break ;
    default : return 00 ;
  }
}
void sendnum(int num) {
  int array[temp] ;
  for(int i = temp-1 ; i >= 0 ; i--) {
    array[i] = num % 2 ;
    num /= 2 ;
  }
  for(int i = 0 ; i < temp ; i++) {
    printf("%d",array[i]) ;
  }
}
int main() {
  /*
  char input ;
  scanf("%c", &input) ;
  // printf("%d\n", input) ;
  int half1, half2 ;
  half1 = input / 16 ;
  half2 = input % 16 ;

  int array[10] ;
  // printf("%d %d \n", half1, half2) ;
  // printf("%d %d \n", encoder(half1), encoder(half2)) ;
  int encoded = encoder(half1) * 32 + encoder(half2) ;
  // printf("%d", encoded) ;
  for(int i = 0 ; i < 10 ; i++) {
    array[9-i] = encoded % 2 ;
    encoded /= 2 ;
  }
  for(int i = 0 ; i < 10 ; i++) {
    printf("%d ", array[i]);
  }
  */
  sendnum((int)'S') ;
  return 0 ;
}
