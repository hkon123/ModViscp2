#include <stdlib.h>
#include <stdio.h>
#include <getopt.h>
#include <unistd.h>
#include <ctype.h>


int infNeigh(int state[50][50], int index1, int index2);
float getInfFrac(int state[50][50]);
int printState(int state[50][50]);
float sirs(float p1, float p3, int sweeps, float immuneFraction);

int main(int argc, char **argv){


  int status;
  status = remove("newFraction.txt");
  status = remove("newVariance.txt");

  int dimflag = 20;
  int sweepflag = 1000;
  int immuneFlag = 0;
  int index;
  int c;


  opterr = 0;

  while ((c = getopt (argc, argv, "blsci")) != -1)
   switch (c)
     {
     case 'b':
      dimflag = 50;
      break;
     case 'l':
      sweepflag = 10000;
      break;
     case 's':
      dimflag = 10;
      break;
    case 'i':
      immuneFlag = 1;
      break;
     case 'c':
      printf("Dimensions of countour:");
      scanf("%d", &dimflag);
      printf("How many sweeps?");
      scanf("%d", &sweepflag);
      break;
     case '?':
      if (isprint (optopt))
        fprintf (stderr, "Unknown option `-%c'.\n", optopt);
        else
          fprintf (stderr,
                  "Unknown option character `\\x%x'.\n",
                  optopt);
       return 1;
     default:
       abort ();
     }

     for (index = optind; index < argc; index++)
      printf ("Non-option argument %s\n", argv[index]);

  int i,j,dimensions, current, total;
  float p1,p3,increment,immuneFraction;
  p1 = 0;
  p3 = 0;
  dimensions = dimflag;
  increment = 1.0/dimensions;
  current = 0;
  total = dimensions*dimensions;
  immuneFraction = 0;
  float results = 0;

  if(immuneFlag==0){
    for(i=0 ; i<dimensions ; i++){
      p3 = 0;
      for(j=0 ; j<dimensions ; j++){
        results = sirs(p1,p3, sweepflag,0);
        printf("%d/%d\n", current,total);
        p3 = p3 + increment;
        current++;
      }
      p1 = p1 + increment;
      FILE *f = fopen("newFraction.txt", "a+");
      fprintf(f,"\n");
      fclose(f);

      FILE *v = fopen("newVariance.txt", "a+");
      fprintf(v,"\n");
      fclose(v);
    }
  }
  else{
    for(i=0 ; i<100 ; i++){
      results = sirs(0.5,0.5,sweepflag,immuneFraction);
      immuneFraction = immuneFraction + 0.01;
      printf("%d/100\n",current );
      current++;
    }
  }

  return 0;
}



float sirs(float p1, float p3, int sweeps, float immuneFraction){

  int iterations, dimensions, equilibration, sampleStep, i, j, check, count, test, count2;
  float p2,fract, fractAvrg, squareFractAverage, variance;
  iterations = sweeps;
  dimensions = 50;
  equilibration = 100;
  sampleStep = 10;
  p2 = 0.5;
  count = 0;
  count2 = 0;
  fractAvrg = 0;
  squareFractAverage =0;

  int immune = 0;
  int maxImmune = dimensions*dimensions*immuneFraction;
  float immuneProb;

  float infectedFraction[(iterations-equilibration)/sampleStep];
  int state[50][50] = {{0}};

  for( i=0; i<dimensions ; i++){
    for( j=0; j<dimensions ; j++){
      int r1 = (rand()%1000);
      float r = r1;
      r = r/1000;
      if (r<=0.33){
        state[i][j] = 1;
      }
      else if (r>0.33 && r<=0.66){
        state[i][j] = 0;
      }
      else{
        state[i][j] = -1;
      }
    }
  }
  if(immuneFraction!=0){
    while(immune<maxImmune){
      for( i=0; i<dimensions ; i++){
        for( j=0; j<dimensions ; j++){
          float r2 = (rand()%1000);
          r2 = r2/1000;
          if(r2<=0.1){
            state[i][j] = -2;
            immune++;
          }
        }
      }
    }
  }

  for( i=0 ; i<iterations ; i++){
    for( j=0 ; j<50*50 ; j++){
      float r = (rand()%1000);
      r = r/1000;
      int index1 = (rand()%50);
      int index2 = (rand()%50);
      if(state[index1][index2] == 1 && r<=p1){
        check = infNeigh(state, index1,index2);
        if(check == 0){
          state[index1][index2] = 0;
          continue;
        }
      }
      else if(state[index1][index2] == 0 && r<=p2){
        state[index1][index2] = -1;
        continue;
      }
      else if(state[index1][index2] == -1 && r<=p3){
        state[index1][index2] = 1;
        continue;
      }
    }
    if(i==equilibration || (i>equilibration && i%sampleStep==0)){
      fract = getInfFrac(state);
      infectedFraction[count] = fract;
      count++;
    }
  }

  for(i=0 ; i<(iterations-equilibration)/sampleStep ; i++){
    fractAvrg = fractAvrg + infectedFraction[i];
    squareFractAverage = squareFractAverage + infectedFraction[i]*infectedFraction[i];
    count2++;
    }
  fractAvrg = fractAvrg/count2;
  squareFractAverage = squareFractAverage/count2;
  variance = squareFractAverage - fractAvrg*fractAvrg;

  FILE *f = fopen("newFraction.txt", "a+");
  fprintf(f,"%f ",fractAvrg);
  fclose(f);

  FILE *v = fopen("newVariance.txt", "a+");
  fprintf(v,"%f ",variance);
  fclose(v);



  return variance;
}

int infNeigh(int state[50][50], int index1, int index2){
  int dimensions = 50;
  if(state[(index1-1)%dimensions][index2] == 0){
    return 0;
  }
  else if (state[index1][(index2+1)%dimensions] == 0){
    return 0;
  }
  else if (state[(index1+1)%dimensions][index2] == 0){
    return 0;
  }
  else if (state[index1][(index2-1)%dimensions] == 0){
    return 0;
  }
  else {
    return 1;
  }


}

float getInfFrac(int state[50][50]){
  float infSum = 0;
  int i,j;
  for( i=0; i<50 ; i++){
    for( j=0; j<50 ; j++){
      if(state[i][j] == 0){
        infSum++;
      }
    }
  }
  float fraction = infSum/(50*50);
  return fraction;
}

int printState(int state[50][50]){
  int i,j;
  for( i=0; i<50 ; i++){
    for( j=0; j<50 ; j++){
      printf("%d ", state[i][j]);
    }
    printf("\n");
  }
  printf("\n\n\n\n--------------------------\n\n\n\n\n");
  return 0;
}
