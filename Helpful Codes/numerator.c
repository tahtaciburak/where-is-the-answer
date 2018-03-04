#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 1024
//#define input "x.txt"
#define answers "AnswersSentences.txt" 
#define sentenceInLines "EachRowOneSentence.txt"
#define trueAnswers "AnswersNumbered.txt"
#define TEXT_SIZE (N*N)
#define numOfAnswers 10


int isFilePointerNull(FILE*, char*);
void printDashes();

int main(){
	int i,j,k;
	int sentenceCount;
	int strLength;
	char *str;
	char text[TEXT_SIZE];
	char** sentences;
	char tmpStr[N], tmpStr2[N];
	int *whichSentence;
	char input[32];

	scanf("%s",input);
	strcat(input,".txt");

	FILE *fp1,*fp2, *fp3, *fp4;	

	str =(char*) malloc( N * sizeof(char));

	fp1 = fopen(input,"r");
	if(isFilePointerNull(fp1,input)) return -1;


	fp3 = fopen(sentenceInLines,"w+");
	if(isFilePointerNull(fp3,sentenceInLines)) return -2;



	for(sentenceCount=0; fgets (str, N, fp1)!=NULL;sentenceCount++ ) {
		strcat(text,str);
	}
	strLength =(int)strlen(text);


	sentenceCount =1;
	fprintf(fp3,"%c",text[0]);
	for(i=1,sentenceCount=2;i<strLength;i++){
		if(text[i] == '"'){
			fprintf(fp3,"\"");
			i++;
			while(text[i] != '"'){
				fprintf(fp3,"%c",text[i]);
				i++;
			}
		}
		if(text[i] == '.'){

			for(i = i+1;text[i]== ' ';i++);
				i--;
			//printf(".\n%d. ",sentenceCount);
			fprintf(fp3,".\n"); // new line
			sentenceCount++;	
		}
		else if(text[i] == '?'){

			for(i = i+1;text[i]== ' ';i++);
				i--;
			//printf(".\n%d. ",sentenceCount);
			fprintf(fp3,"?\n"); // new line
			sentenceCount++;	
		}


		else if(text[i] != '\n')
			fprintf(fp3,"%c",text[i]);
	}
	fclose(fp1);
	fclose(fp3);
	fp3 = fopen(sentenceInLines, "r");
	
	printf("%d\n",sentenceCount-2);
	sentenceCount = sentenceCount-2;



	sentences=(char**) malloc(sentenceCount*sizeof(char*));
	for(i=0;i<sentenceCount;i++){
		sentences[i] = (char*) malloc(N * sizeof(char));
	}


	for(i=0; i< sentenceCount && fgets (str, N, fp1)!=NULL;i++ ) {
		str[strlen(str)-1] = '\0';
		strcpy(sentences[i],str);
	}

	

	for(i=0; i< sentenceCount;i++ ) {
		printf("%d.<<%s>>\n",(i+1),sentences[i]);
	}
	fclose(fp3); // We are done with fp3

	fp4 = fopen(trueAnswers, "w");
	if(isFilePointerNull(fp4,trueAnswers)) return -3;

	fp2 = fopen(answers,"r+");
	if(isFilePointerNull(fp2,answers)) return -4;

	whichSentence = (int*)malloc(numOfAnswers * sizeof(int));
	for(i=0;i<sentenceCount;i++)	// initiate whichSentence
		whichSentence[i] = -1;
	// printDashes();
	for(i=0;fgets (str, N, fp2)!=NULL;i++ ){
		str[strlen(str)-1] = '\0';
		puts(str);

		printDashes();
		for(j=0;j< sentenceCount;j++){

			strcpy(tmpStr,sentences[j]);
			strcpy(tmpStr2,str);
			
			tmpStr[strlen(sentences[j])/2] = '\0';
			tmpStr2[strlen(sentences[j])/2] = '\0';

			if(strcmp(tmpStr, tmpStr2) == 0){
				printf("%d.\n<%s>\nAND\n<%s>\nARE SAME\n\n",j,sentences[j],str);
				whichSentence[i] = j+1;			
			}
			else
				;//printf("<%s>\nAND\n<%s>\nARE NOT SAME\n\n",sentences[j],str);
		}
		printDashes();

		

	} 
	
	for(i=0;i<numOfAnswers;i++){	// initiate whichSentence
		printf("%d.answer is in %d.sentence.\n",(i+1),whichSentence[i]);
		fprintf(fp4,"%d\n",whichSentence[i]);
	}

	
	free(whichSentence);
	//fclose(fp2);
	//fclose(fp4);

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