#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

void print_flag() {
    char otp[] = {161, 143, 215, 178, 242, 250, 72, 57, 107, 194, 146, 16, 88, 68, 101, 140, 74, 117, 86, 11, 102, 81, 104, 137, 141, 12, 253, 141, 103, 34, 223, 15, 202, 143, 155, 37, 185};
    char data[] = {170, 47, 229, 88, 184, 106, 60, 51, 21, 214, 88, 66, 56, 49, 98, 222, 205, 164, 233, 184, 232, 189, 252, 119, 162, 137, 122, 193, 162, 218, 51, 55, 216, 75, 157, 185, 20};
    size_t len = sizeof(data) / sizeof(data[0]);
    
    for (int i = len-1; i > 0; i--) {
        data[i] = data[i-1] ^ data[i];
    }

    for (int i = 0; i < len; i++) {
        data[i] = data[i] ^ 0x69;
    }

    for (int i = 0; i < len; i++) {
        data[i] = otp[i] ^ data[i];
    }

    puts(data);
}

void msleep(unsigned int sec, unsigned int millis) {
    return;
    struct timespec remaining, request = {sec, millis*1000000};
    nanosleep(&request, &remaining);
}

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IONBF, 0);
    srand(time(NULL));

    if (argc != 2) {
        printf("Every question has answer... if you know how to ask\n");
        printf("Go ahead, ask me anything.\n", *argv);
        exit(0);
    }

    int is_magic = 0;

    if (!strcmp(*argv, "./magic8ball")) {
        printf("Why, I guess you're right... I am magic :D\n");
        is_magic = 1;
    }

    char *responses[] = {
        "Outlook not so good.",
        "It's unclear at this time.",
        "Ask again later.",
        "Signs point to uncertainty.",
        "Reply hazy, try again.",
        "The future is uncertain.",
        "It's not looking promising.",
        "Cannot predict now.",
        "You might want to reconsider.",
        "My sources say no.",
        "I'm not certain about that.",
        "It's a toss-up.",
        "The answer is elusive.",
        "Try again in the future.",
        "Don't get your hopes up.",
        "It's not in the cards.",
        "Results are doubtful.",
        "The outcome is iffy.",
        "Things are unclear.",
        "Ask someone else.",
        "The prospects are dim.",
        "Keep your options open.",
        "Signs are inconclusive.",
        "It's a murky situation.",
        "The path is uncertain.",
        "You'll have to wait and see.",
        "It's anyone's guess.",
        "The chances are slim.",
        "The future is shrouded.",
        "You may want to reconsider.",
        "It's too early to tell.",
        "Outlook uncertain.",
        "The response is muddled.",
        "Consider other options.",
        "Signs are not favorable.",
        "My sources are hesitant.",
        "The outcome is fuzzy.",
        "Keep your expectations low.",
        "It's not looking good.",
        "Try again another time."
    };

    printf("You asked:\n");
    msleep(0, 500);

    printf("\"%s\"\n", *(argv+1));
    msleep(1, 0);
    printf("Hmmm");
    msleep(1, 0);
    printf(".");
    msleep(1, 0);
    printf(".");
    msleep(1, 0);
    printf(".");
    msleep(1, 0);
    printf(".\n");
    msleep(2, 0);

    if (is_magic && strstr(*(argv+1), "flag")) {
        printf("Why yes, here is your flag!\n");
        print_flag();
    } else {
        size_t num_of_elms = sizeof(responses) / sizeof(responses[0]);

        int num = rand() % num_of_elms;
        puts(responses[num]);
    }
}

