#include <stdio.h>

#ifndef FLAG
#define FLAG ""
#endif

int main() {
  printf("Welcome to the Smederij Smithy! 🔨\n");

  while (1) {
    printf("\nWhat do you want to do?\n"
           "1) Forge\n"
           "2) Hammer\n"
           "3) Draw\n"
           "4) Upset\n"
           "5) Bend\n"
           "6) Punch\n"
           "7) Flag\n");
    char choice = getchar();
    getchar(); // get newline
    switch (choice) {
    case '1':
      printf("You heat up the metal.\n");
      break;
    case '2':
      printf("You bend the metal in to shape ever so slightly.\n");
      break;
    case '3':
      printf("You grab your tongs and stretch out the metal.\n");
      break;
    case '4':
      printf("You make your metal thicker and shorter.\n");
      break;
    case '5':
      printf("You put a slight curve in the metal.\n");
      break;
    case '6':
      printf("You punch a hole in the metal.\n");
      break;
    case '7':
      printf("You make a flag out of the metal. " FLAG "\n");
      break;
    default:
      printf("You do nothing.\n");
      break;
    }
  }

  return 0;
}
