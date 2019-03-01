#include <stdlib.h>
#include <stdio.h>


int infNeigh(int state[50][50], int index1, int index2);
float getInfFrac(int state[50][50]);
int printState(int state[50][50]);
float sirs(float p1, float p3);
float sirsV(float p1, float p3);

int main(void){

  int i,j,dimensions, current, total;
  float p1,p3,increment;
  p1 = 0;
  p3 = 0;
  dimensions = 20;
  increment = 1.0/dimensions;
  current = 0;
  total = dimensions*dimensions;
  float results[20][20] = {{0}};

  for(i=0 ; i<dimensions ; i++){
    p3 = 0;
    for(j=0 ; j<dimensions ; j++){
      results[i][j] = sirsV(p1,p3);
      printf("%d/%d\n", current,total);
      p3 = p3 + increment;
      current++;
    }
    p1 = p1 + increment;
  }
  FILE *f = fopen("testing.txt", "w");
  for(i=0 ; i<dimensions ; i++){
    for(j=0 ; j<dimensions ; j++){
      fprintf(f,"%f ",results[i][j]);
    }
    fprintf(f,"\n");
  }
  fclose(f);


  return 0;
}


float sirs(float p1, float p3){

  int iterations, dimensions, equilibration, sampleStep, i, j, check, count, test, count2;
  float p2,fract, fractAvrg;
  iterations = 1000;
  dimensions = 50;
  equilibration = 100;
  sampleStep = 10;
  p2 = 0.5;
  count = 0;
  count2 = 0;
  fractAvrg = 0;

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
    count2++;
  }
  fractAvrg = fractAvrg/count2;

  return fractAvrg;
}

float sirsV(float p1, float p3){

  int iterations, dimensions, equilibration, sampleStep, i, j, check, count, test, count2;
  float p2,fract, fractAvrg, squareFractAverage, variance;
  iterations = 1000;
  dimensions = 50;
  equilibration = 100;
  sampleStep = 10;
  p2 = 0.5;
  count = 0;
  count2 = 0;
  fractAvrg = 0;
  squareFractAverage =0;

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
