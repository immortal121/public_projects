/*
Name of programmer : Rohith Yarramala
Language : c
Name of project : bug manager
*/
// header declared here
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
// functions declaration here
void printbanner(char s[]);
void fileabug(void);
void viewabug(void);
// void checkstatusofbug(void);
void listbugs(void);
// void changestatusofbug(void);
void deleteabug(void);
void searchabug(char s[], char[]);
void show_options(void);
// void replaceAll(char *str, const char *oldWord, const char *newWord);
void main()
{
    system("cls");
    int looper = 1;
    int task;
    FILE *filedata;
    if (fopen("list.txt", "r") == NULL)
    {
        filedata = fopen("list.txt", "w");
        fseek(filedata, 0, SEEK_END);
        int size = ftell(filedata);
        if (size == 0)
        {
            printf("list.txt is not there Creating.");
            fprintf(filedata, "\tName of bug\t\tDescription of Bug\t\tReported By\t\tstatus\t\tDate & Time\n");
        }
        fclose(filedata);
    }

    char title[] = "WELCOME TO BUG MANAGER";
    char optionvalue[30];
    printbanner(title);

    while (looper)
    {
        printf("\tOPTIONS -");
        printf("\n");
        printf("[+] 1 . File a Bug");
        printf("\n");
        printf("[+] 2 . Check Status of a Bug ");
        printf("\n");
        // printf("[+] 3 . Change Status of a Bug");
        // printf("\n");
        printf("[+] 3 . Delete A Bug");
        printf("\n");
        printf("[+] 4 . List All Bugs");
        printf("\n");
        printf("[+] 5 . Show A Bugs");
        printf("\n");
        printf("[+] 6 . Exit ");
        printf("\n=>");

        scanf("%d", &task);
        task = (int)(task);
        switch (task)
        {
        case 1:
            fileabug();
            looper--;
            break;
        // case 2:
        //     checkstatusofbug();
        //     looper--;
        //     break;
        // case 3:
        //     changestatusofbug();
        //     looper--;
        //     break;
        case 2:
            deleteabug();
            looper--;
            break;
        case 3:
            listbugs();
            looper--;
            break;
        case 4:
            viewabug();
            looper--;
            break;
        case 5:
            printf("Please Wait Exiting ........");
            exit(0);
            break;

        default:
            printf("Please Choose Valid Option");
            exit(0);
            break;
        }
    }
}

// show options ----------------------------------------------------------------
void show_options(void)
{
    int looper = 1, task;
    system("cls");
    while (looper)
    {
        printf("\tOPTIONS -");
        printf("\n");
        printf("[+] 1 . File a Bug");
        printf("\n");
        // printf("[+] 2 . Check Status of a Bug ");
        // printf("\n");
        // printf("[+] 3 . Change Status of a Bug");
        // printf("\n");
        printf("[+] 2 . Delete A Bug");
        printf("\n");
        printf("[+] 3 . List All Bugs");
        printf("\n");
        printf("[+] 4 . Show A Bugs");
        printf("\n");
        printf("[+] 5 . Exit ");
        printf("\n=>");

        scanf("%d", &task);
        task = (int)(task);
        switch (task)
        {
        case 1:
            fileabug();
            looper--;
            break;
        // case 2:
        //     checkstatusofbug();
        //     looper--;
        //     break;
        // case 3:
        //     changestatusofbug();
        //     looper--;
        //     break;
        case 2:
            deleteabug();
            looper--;
            break;
        case 3:
            listbugs();
            looper--;
            break;
        case 4:
            viewabug();
            looper--;
            break;
        case 5:
            printf("Please Wait Exiting ........");
            exit(0);
            break;

        default:
            printf("Please Choose Valid Option");
            exit(0);
            break;
        }
    }
}
// //change status of a bug ----------------------------------------------------
// void changestatusofbug(void){
//       /* File pointer to hold reference of input file */
//     FILE * fPtr;
//     FILE * fTemp;
//     char path[100] = "list.txt";

//     char buffer[1000];
//     char oldWord[100] = "", newWord[100];

//     printf("Enter word to replace: ");
//     scanf("%s", oldWord);

//     printf("Replace '%s' with: ");
//     scanf("%s", newWord);

//     /*  Open all required files */
//     fPtr  = fopen(path, "r");
//     fTemp = fopen("replace.tmp", "w");

//     /* fopen() return NULL if unable to open file in given mode. */
//     if (fPtr == NULL || fTemp == NULL)
//     {
//         /* Unable to open file hence exit */
//         printf("\nUnable to open file.\n");
//         printf("Please check whether file exists and you have read/write privilege.\n");
//         exit(EXIT_SUCCESS);
//     }

//     /*
//      * Read line from source file and write to destination
//      * file after replacing given word.
//      */
//     while ((fgets(buffer, 1000, fPtr)) != NULL)
//     {
//         // Replace all occurrence of word from current line
//         replaceAll(buffer, oldWord, newWord);

//         // After replacing write it to temp file.
//         fputs(buffer, fTemp);

//     }

//     /* Close all files to release resource */
//     fclose(fPtr);
//     fclose(fTemp);

//     /* Delete original source file */
//     remove(path);

//     /* Rename temp file as original file */
//     rename("replace.tmp", path);

// }

// /**
//  * Replace all occurrences of a given a word in string.
//  */
// void replaceAll(char *str, const char *oldWord, const char *newWord)
// {
//     char *pos, temp[1000];
//     int index = 0;
//     int owlen;

//     owlen = strlen(oldWord);

//     // Fix: If oldWord and newWord are same it goes to infinite loop
//     if (!strcmp(oldWord, newWord)) {
//         return;
//     }

//     /*
//      * Repeat till all occurrences are replaced.
//      */
//     int i = 1;

//     while ((pos = strstr(str, oldWord)) != NULL && (i != 0))
//     {
//         // Backup current line
//         strcpy(temp, str);

//         // Index of current found word
//         index = pos - str;

//         // Terminate str after word found index
//         str[index] = '\0';

//         // Concatenate str with new word
//         strcat(str, newWord);

//         // Concatenate str with remaining words after
//         // oldword found index.
//         strcat(str, temp + index + owlen);
//         // exit(1);
//         i--;
//     }

// }
// Delete a bug --------
void deleteabug(void)
{
    FILE *fp, *temp;
    char getname[20], var[400], search_string[100], line[200], c;
    int i = 1;
    printf("\tEnter Name of Bug\n=>");
    scanf("%s", &getname);
    strcpy(search_string, getname);
    strcat(getname, ".txt");
    fp = fopen("list.txt", "r");
    temp = fopen("temp.txt", "w");
    while (fgets(line, 200, fp) != NULL) /* read a line */
    {
        if (strstr(line, search_string))
        {
            break;
        }
        i++;
    }
    char buffer[1000];
    int count = 1, l;
    l = i;
    rewind(fp);
    while ((fgets(buffer, 1000, fp)) != NULL)
    {
        if (l != count)
            fputs(buffer, temp);
        count++;
    }
    fclose(fp);
    remove(getname);
    fclose(temp);
    FILE *fpp, *tempp;
    char ch;
    tempp = fopen("temp.txt", "r");
    fpp = fopen("list.txt", "w");
    rewind(fpp);
    rewind(temp);
    while ((ch = fgetc(tempp)) != EOF)
    {
        fputc(ch, fpp);
    }
    fclose(fpp);
    fclose(tempp);
    remove("temp.txt");
    int opt;
    printf("\nEnter \n1 . Show Options \n2 . Delete a Bug \n3 . Exit\n=>");
    scanf("%d", &opt);
    switch (opt)
    {
    case 1:
        show_options();
        break;
    case 2:
        deleteabug();
        break;
    case 3:
        printf("Exiting .....");
        exit(0);
        break;

    default:
        printf("Please Choose Valid Option");
        exit(0);
        break;
    }
}

// show a bug -----------------------------------------------------------------
void viewabug(void)
{
    system("sys");
    printbanner("View a Bug");
    FILE *fp;
    char getname[20], var[400], c;
    printf("Enter Name of Bug\n=>");
    scanf("%s", &getname);
    strcat(getname, ".txt");
    fp = fopen(getname, "r");
    if (fp != NULL)
    {
        c = fgetc(fp);
        while (c != EOF)
        {
            printf("%c", c);
            c = fgetc(fp);
        }
    }
    else
    {
        printf("!NO Record Found With The Given Name");
    }
    fclose(fp);
    int opt;
    printf("\nEnter \n1 . Show Options \n2 . Show a Bug \n3 . Exit\n=>");
    scanf("%d", &opt);
    switch (opt)
    {
    case 1:
        show_options();
        break;
    case 2:
        viewabug();
        break;
    case 3:
        printf("Exiting .....");
        exit(0);
        break;

    default:
        printf("Please Choose Valid Option");
        exit(0);
        break;
    }
}
// list bugs -------------------------------------------------------------------------
void listbugs(void)
{
    printbanner("List ALL Bugs");
    FILE *fp;
    int i = 1;
    char line[200];
    fp = fopen("list.txt", "r");
    while (fgets(line, 200, fp) != NULL) /* read a line */
    {
        printf("%d", i);
        printf("%s", line); /* write the line */
        i++;
    }
    int opt;
    printf("\nEnter \n1 . Show Options \n2 . Exit\n=>");
    scanf("%d", &opt);
    switch (opt)
    {
    case 1:
        show_options();
        break;
    case 2:
        printf("Exiting .....");
        exit(0);
        break;

    default:
        printf("Please Choose Valid Option");
        exit(0);
        break;
    }
}
// search a bug ---------------------------------------------------------------------
void searchabug(char s[], char fname[256])
{

    FILE *fp;
    char filename[200], line[200], search_string[12];
    strcpy(filename, fname);
    strcpy(search_string, s);
    fp = fopen(fname, "r");
    if (!fp)
    {

        perror("could not find the file");

        exit(0);
    }

    while (fgets(line, 200, fp) != NULL) /* read a line */
    {

        if (strstr(line, search_string))
        {

            fputs(line, stdout); /* write the line */

            break;
        }
    }
    int opt;
    fclose(fp);
    printf("\nEnter \n2 . Show Options \n3 . Exit\n=>");
    scanf("%d", &opt);
    switch (opt)
    {
    
    case 1:
        show_options();
        break;
    case 2:
        printf("Exiting .....");
        exit(0);
        break;

    default:
        printf("Please Choose Valid Option");
        exit(0);
        break;
    }
}
// check status ---------------------------------------------------------------------
// void checkstatusofbug(void)
// {
//     char s[20], fname[10] = "list.txt";
//     printf("Enter Name of Bug\n=>");
//     scanf("%s", &s);
//     searchabug(s, "list.txt");
// }
// file a bug ----------------------------------------------------------------------
void fileabug(void)
{
    char name[20], desc[100], rname[20];
    int opt;
    printbanner("File a Bug");
    printf("\tEnter Name of Bug :\n\t=>");
    scanf("%s", &name);
    printf("\tEnter Name of Reporter :\n\t=>");
    scanf("%s", &rname);
    printf("\tEnter Description of Bug(max 100 words) :\n\t=>");
    scanf("%s", &desc);
    char tempname[20];
    strcpy(tempname, name);
    strcat(tempname, ".txt");
    FILE *newfile = fopen(tempname, "w");
    fprintf(newfile, "Date of Bug Created : %s\n", __DATE__);
    fprintf(newfile, "Time of Bug Created : %s\n", __TIME__);
    fprintf(newfile, "Name of Bug :\t%s\n", name);
    fprintf(newfile, "Bug Reported By:\t%s\n", rname);
    fprintf(newfile, "Description of Bug :\t%s\n", desc);
    fclose(newfile);
    FILE *appendfile = fopen("list.txt", "a+");
    fprintf(appendfile, "\n\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s", name, desc, rname, "Not Viewed", __DATE__, __TIME__);
    fclose(appendfile);
    printf("Date of Bug Created : %s\n", __DATE__);
    printf("Time of Bug Created : %s\n", __TIME__);
    printf("Name of Bug :\t%s\n", name);
    printf("Bug Reported By:\t%s\n", rname);
    printf("Description of Bug :\t%s\n", desc);
    printf("\nEnter \n1 . File a Bug\n2 . Show Options \n3 . Exit\n=>");
    scanf("%d", &opt);
    switch (opt)
    {
    case 1:
        fileabug();
        break;
    case 2:
        show_options();
        break;
    case 3:
        printf("Exiting .....");
        exit(0);
        break;

    default:
        printf("Please Choose Valid Option");
        exit(0);
        break;
    }
}
// banner -----------------------------------------------------------------------------
void printbanner(char s[])
{
    system("cls");
    printf("\n");
    for (int i = 0; i <= 35; i++)
    {
        printf("*");
    }
    printf("\n");
    int len = strlen(s);
    int redux = floor((35 - len) / 2);
    // for (int i = 0; i <= 15; i++)
    // {
    for (int j = 0; j < redux; j++)
    {
        printf("*");
    }
    printf("  ");
    printf("%s", s);
    printf("  ");
    for (int j = len + redux + 4; j <= 35; j++)
    {
        printf("*");
    }

    // }
    printf("\n");
    for (int i = 0; i <= 35; i++)
    {
        printf("*");
    }
    printf("\n");
}