#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 1024
//#define input "x.txt"
#define trueAnswers "AnswersNumbered.txt"
#define TEXT_SIZE (N*N)
#define numOfAnswers 10

int isFilePointerNull(FILE*, char*);
void printDashes();

int main(){
	int i;
	FILE *fp, *fp2;
	char input[32];
	char output[32];
	char str[1000];
	char newText[TEXT_SIZE];

	scanf("%s",input);
	strcpy(output,input);

	strcat(input,".txt");
	strcat(output,"NEW.txt");

	strcpy(newText,"");

	fp = fopen(input,"r");
	if(isFilePointerNull(fp,input)) return -1;


	fp2 = fopen(output,"w");
	if(isFilePointerNull(fp2,output)) return -2;

	while(fgets(str,N,fp) != NULL){
		for(i=0;i<strlen(str);i++){
			//if(str[i] == '”' or str[i]== '“')
			//	str[i]='"';


		}
		printf(" a \n" );

		strcat(newText,str);
		//puts(str);
	}

	fprintf(fp2, "%s",newText );
	printf("Success\n");
	return 0;
}



int isFilePointerNull(FILE *fp, char* fileName){
	if(fp == NULL){
		printf("%s cannot be opened.\n",fileName );
		return 1;
	}
	else
		return 0;
}

void printDashes(){
	printf("----------------------\n");

}