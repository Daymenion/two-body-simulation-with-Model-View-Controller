#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double initial_eccentricity = 0.6;
double initial_q = 0.11;
FILE* writen;



typedef struct {
    double x;
    double y;
}Body;

typedef struct
{

    double u[4];
    Body *Planet1;
    Body *Planet2;
    double mass1;
    double mass2;
    double mass12;
    double eccentricity; // Eccentricity of the orbit
    double q; // Mass ratio m2 / m1

} TwoBodyModel;

typedef void (*f_void_x)(TwoBodyModel*);

typedef struct
{
    f_void_x display;
} TwoBodyView;

typedef struct
{
    TwoBodyModel* model;
    TwoBodyView* view;

} TwoBodyController;

void console_display(TwoBodyModel this)
{
    fprintf(writen,"Planet1 ---> x = %-6lf\ty = %-6lf\t||\t",this.Planet1->x,this.Planet1->y);
    fprintf(writen,"Planet2 ---> x = %-6lf\ty = %-6lf\n",this.Planet2->x,this.Planet2->y);
}


void create_console_view(TwoBodyView* this)
{
    this->display = (f_void_x) console_display;
}

double initialVelocity(double q, double eccentricity) {
    return sqrt( (1 + q) * (1 + eccentricity) );
}


void reset_state_to_initial_conditions(TwoBodyController *this) {
    this->model->q = initial_q;
    this->model->eccentricity = initial_eccentricity;

    this->model->u[0]  = 1.0;
    this->model->u[1]  = 0.0;
    this->model->u[2]  = 0.0;
    this->model->u[3]  = initialVelocity(this->model->q,this->model->eccentricity);

    this->model->mass1 = 1.0;
    this->model->mass2 = this->model->q;
    this->model->mass12 = this->model->mass1 + this->model->mass2;


    this->model->Planet1->x =0;
    this->model->Planet2->x =0;
    this->model->Planet1->y =0;
    this->model->Planet2->y =0;
}

double* derivative(TwoBodyController *this) {
    double *du = malloc(4* sizeof(double));
    double r[2] = {(this->model->u[0]),(this->model->u[1])};

    double rr = sqrt(pow(r[0],2) + pow(r[1],2));

    for (int i =0; i<2; i++) {
        du[i] = this->model->u[i+2];
        du[i+2] = -(1 + this->model->q) * r[i] / pow(rr,3);
    }
    return du;
}
void Runge_kutta_calculate(TwoBodyController *this,double h) {
    double a[4] = {h/2,h/2,h,0};
    double b[4] = {h/6,h/3,h/3,h/6};
    double u0[4];
    double ut[4];
    double *du;
    for (int i = 0; i < 4; i++) {
        u0[i] = *(this->model->u+ i);
        ut[i] = 0;
    }
    for (int j = 0; j < 4; j++) {
        du = derivative(this);
        for (int i = 0; i < 4; i++) {
            this->model->u[i] = u0[i] + a[j] * du[i];
            ut[i] = ut[i] + b[j] * du[i];
        }
    }
    for (int i = 0; i < 4; ++i)
        this->model->u[i] = u0[i] + ut[i];
}

void calculate_new_position(TwoBodyController *this){
    double r = 1.0;

    double a1 = (this->model->mass2 / this->model->mass12) *r;
    double a2 = (this->model->mass1 / this->model->mass12) *r;

    this->model->Planet1->x = -a2 * this->model->u[0];
    this->model->Planet1->y = -a2 * this->model->u[1];
    this->model->Planet2->x = a1 * this->model->u[0];
    this->model->Planet2->y = a1 * this->model->u[1];
}

void uptade_position(TwoBodyController *this) {
    double timestep=0.15;
    Runge_kutta_calculate(this, timestep);

    calculate_new_position(this);
}
int main()
{
    writen = fopen("AnalysisResult.txt", "w");

    Body planet1;
    Body planet2;
    TwoBodyModel model;
    TwoBodyView view;
    TwoBodyController controller;

    controller.model = &model;
    controller.view = &view;
    controller.model->Planet1 = &planet1;
    controller.model->Planet2 = &planet2;

    create_console_view(&view);
    reset_state_to_initial_conditions(&controller);

    for (int i = 0; i < 1000; ++i) {
        uptade_position(&controller);
        controller.view->display(controller.model);
    }

    fclose(writen);

    return 0;
}