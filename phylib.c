//C code file for A2 CIS2750
//Header File include
#include "phylib.h"
//New Still Ball Function
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos){
    //Mallocing and checking for NULL or malloc failure
    phylib_object * newStillBall = (phylib_object *) malloc(sizeof(phylib_object));

    if(newStillBall == NULL){
        return NULL;
    }
    //Updating values in new object and returning
    newStillBall->type = PHYLIB_STILL_BALL;

    newStillBall->obj.still_ball.number = number;

    newStillBall->obj.still_ball.pos = *pos;

    return newStillBall;

}
//New Rolling Ball Function
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc){
    //Mallocing for a phylib_object then checking for allocation failure or NULL Pointer
    phylib_object * newRollBall = (phylib_object *)malloc(sizeof(phylib_object));

    if(newRollBall == NULL){
        return NULL;
    }
    //Updating values of new roll ball and returning
    newRollBall->type = PHYLIB_ROLLING_BALL;

    newRollBall->obj.rolling_ball.number = number;
    newRollBall->obj.rolling_ball.pos = *pos;
    newRollBall->obj.rolling_ball.vel = *vel;
    newRollBall->obj.rolling_ball.acc = *acc;

    return newRollBall;
}
//New Hole Function
phylib_object * phylib_new_hole(phylib_coord *pos){
    //Allocating memory for a new hole phylib_object then handling any memory/allocation/null pointer errors,
    phylib_object * newHole = (phylib_object *)malloc(sizeof(phylib_object));

    if(newHole == NULL){
        return NULL;
    }
    //Updating the newly created hole
    newHole->type = PHYLIB_HOLE;
    newHole->obj.hole.pos = *pos;
    return newHole;
}
//New HCushion function
phylib_object * phylib_new_hcushion(double y){
    //Allocating memory for new h cushion and handling any errors
    phylib_object * newHCushion = (phylib_object *)malloc(sizeof(phylib_object));
    
    if(newHCushion == NULL){
        return NULL;
    } 
    //Updating new hole with values before returning
    newHCushion->type = PHYLIB_HCUSHION;
    newHCushion->obj.hcushion.y = y;

    return newHCushion;
}
//New Vcushion function
phylib_object * phylib_new_vcushion(double x){
    //Allocating for a new phylib_object for v cushion then handling any errors.
    phylib_object * newVCushion = (phylib_object *)malloc(sizeof(phylib_object));
    if(newVCushion == NULL){
        return NULL;
    }
    //Updating the object before returning
    newVCushion->type = PHYLIB_VCUSHION;
    newVCushion->obj.vcushion.x = x;

    return newVCushion;
}
//New table function
phylib_table * phylib_new_table(void){
    //Allocating memory for a phylib_table then checking for any allocation errors, or null pointer errors.
    phylib_table * newTable = (phylib_table *)malloc(sizeof(phylib_table));
    int i;
    if(newTable == NULL){
        return NULL;
    }
    //Updating the first 4 indexs with the cushions and setting time to zero.
    newTable->time = 0.0;
    newTable->object[0] = phylib_new_hcushion(0.0);
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    newTable->object[2] = phylib_new_vcushion(0.0);
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    //Calculating hole positions
    phylib_coord topLeft = {0.0, 0.0};
    phylib_coord topRight = {PHYLIB_TABLE_WIDTH, 0.0};
    phylib_coord midLeft = {0.0, (PHYLIB_TABLE_LENGTH / 2)};
    phylib_coord midRight = {PHYLIB_TABLE_WIDTH, (PHYLIB_TABLE_LENGTH / 2)};
    phylib_coord botLeft = {0.0, PHYLIB_TABLE_LENGTH};
    phylib_coord botRight = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH};
    //Setting Hole positions in the next 6 indices (4 - 9)
    newTable->object[4] = phylib_new_hole(&topLeft);
    newTable->object[5] = phylib_new_hole(&midLeft);
    newTable->object[6] = phylib_new_hole(&botLeft);
    newTable->object[7] = phylib_new_hole(&topRight);
    newTable->object[8] = phylib_new_hole(&midRight);
    newTable->object[9] = phylib_new_hole(&botRight);
    //Setting rest of the indices to NULL as they are reserved for the balls, balls are not set in this function
    for(i = 10; i < PHYLIB_MAX_OBJECTS; i++){
        newTable->object[i] = NULL;
    }
    return newTable;
}
//Copy Object Function
void phylib_copy_object(phylib_object **dest, phylib_object **src){
    //Allocating memory for copy object
    phylib_object * cpyObj = (phylib_object *)malloc(sizeof(phylib_object));

    if(cpyObj == NULL){
        return;
    }
    //If src is null just update destination to NULL else memcpy cpyObj with source then update dest with cpyObj
    if(*src == NULL){
        *dest = NULL;
    }else{
        memcpy(cpyObj, *src, sizeof(phylib_object));
        *dest = cpyObj;
    }

}
//Phylib Copy table function
phylib_table *phylib_copy_table(phylib_table *table){
    //Allocating memory for a phylib table. Using Calloc as malloc gave memory errors (unintilizations issues) so using Calloc will intilize the objects
    phylib_table * cpyTable = (phylib_table *)calloc(PHYLIB_MAX_OBJECTS, sizeof(phylib_table));
    if(cpyTable == NULL || table == NULL){
        return NULL;
    }
    //Copying each object from table into cpyTable if null just skip and set cpyTable obj at index to null. 
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] != NULL){
            phylib_copy_object(&cpyTable->object[i], &table->object[i]);
        }else{
            cpyTable->object[i] = NULL;
        }
    }
    cpyTable->time = table->time;
    //memset(cpyTable, 0, PHYLIB_MAX_OBJECTS * sizeof(phylib_object *));
    //*cpyTable = *table;
    return cpyTable;
}
//Add Object to table function
void phylib_add_object(phylib_table *table, phylib_object *object){
    int i;
    //Traversing through the array until null/empty slot is found then adding the object into that slot
    for(i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] == NULL){
            table->object[i] = object;
            break;
        }
    }
}
//Freeing table
void phylib_free_table(phylib_table *table){
    int i;
    //Free each object that is not null then free the whole table itself.
    for(i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] != NULL){
            free(table->object[i]);
        }
    }
    free(table);
}
//Phylib_sub
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2){
    //Subtracting coordinates
    phylib_coord difference;
    
    difference.x = c1.x - c2.x;
    difference.y = c1.y - c2.y;

    return difference;
}
//Length function
double phylib_length(phylib_coord c){
    //Pythagorean theorem basically to find the length
    return sqrt(c.x*c.x + c.y*c.y); 
    // double sum = (c.x * c.x) + (c.y * c.y);
    // sum = sqrt(sum);
    // return sum;
}
//Dot product function
double phylib_dot_product(phylib_coord a, phylib_coord b){
    //Dot product just getting products of x components + products of y components
    // double dotProduct = (a.x * b.x) + (a.y * b.y);
    // return dotProduct;
    // printf("A Values in Dot product, a.x: %f, a.y: %f \n", a.x, a.y);
    // printf("B Values in Dot product, b.x: %2f, b.y: %2f \n", b.x, b.y);
    return (a.x * b.x) + (a.y * b.y);
}
//Some helper functions I made to get the position of different objects (getters/accessors)
phylib_coord getRollingBallPos(phylib_rolling_ball rb){
    return rb.pos;
}

phylib_coord getStillBallPos(phylib_still_ball sb){
    return sb.pos;
}

phylib_coord getHolePos(phylib_hole hole){
    return hole.pos;
}

double getHCush(phylib_hcushion cushion){
    return cushion.y;
}

double getVCush(phylib_vcushion cushion){
    return cushion.x;
}
//Distance functions (Had to use some debug print statements)
double phylib_distance(phylib_object *obj1, phylib_object *obj2) {
    //printf("Seg Check \n");
    double distance = -1.0;
    //Had to add this to make sure no seg fault occurs
    if(obj1 == NULL || obj2 == NULL){
        return -1.0;
    }
    //printf("Check Distance 1 \n")
    //Making sure obj1 is rolling ball
    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }

    // printf("Check Distance 2 \n");
    //printf("Seg Check 2 \n");

    // Calculate the distance based on obj2 type
    //Intilizations made for calculations
    phylib_coord obj1Pos = getRollingBallPos(obj1->obj.rolling_ball);
    phylib_coord obj2Pos = {0,0};
    double hCushObj2 = 0.0;
    double vCush = 0.0;
    //Switch Statement to calculate the distance depending obj2
    switch (obj2->type) {
        case PHYLIB_ROLLING_BALL:
            //If obj2 is rolling ball
            obj2Pos = getRollingBallPos(obj2->obj.rolling_ball);
            distance = phylib_length(phylib_sub(obj1Pos, obj2Pos));
            distance -= PHYLIB_BALL_DIAMETER;
            break;
        case PHYLIB_STILL_BALL:
            //If obj1 is still ball
            obj2Pos = getStillBallPos(obj2->obj.still_ball);
            distance = phylib_length(phylib_sub(obj1Pos, obj2Pos));
            distance -= PHYLIB_BALL_DIAMETER;
            break;
        case PHYLIB_HOLE:
            //If obj2 is a hole
            obj2Pos = getHolePos(obj2->obj.hole);
            distance = phylib_length(phylib_sub(obj1Pos, obj2Pos));
            distance -= PHYLIB_HOLE_RADIUS;
            break;
        case PHYLIB_HCUSHION:
            //if obj2 is a hcushion
            hCushObj2 = getHCush(obj2->obj.hcushion);
            distance = fabs(obj1Pos.y - hCushObj2) - PHYLIB_BALL_RADIUS;
            break;
        case PHYLIB_VCUSHION:
            //If ovj2 is a vcushion
            vCush = getVCush(obj2->obj.vcushion);
            distance = fabs(obj1Pos.x - vCush) - PHYLIB_BALL_RADIUS;
            break;
        default:
            break;
    }
    return distance;
}
//Roll Function
void phylib_roll( phylib_object *new, phylib_object *old, double time){
    //Checking if both passed in object are rolling balls.
    if(new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL){
        return;
    }
    //Creating a newRoll object to update and then set it to new
    //phylib_object * newRollingBall = phylib_new_rolling_ball(old->obj.rolling_ball.number, &old->obj.rolling_ball.pos, &old->obj.rolling_ball.vel, &old->obj.rolling_ball.acc);
    //Calculations made to roll the ball, for position and velocity and acceleration
    //formula: pnew = pold + v(old) * time + 1/2 * a(old) * t^2
    phylib_coord oldPos = getRollingBallPos(old->obj.rolling_ball);
    double newX = oldPos.x + old->obj.rolling_ball.vel.x * time + 0.5 * old->obj.rolling_ball.acc.x * time * time;
    double newY = oldPos.y + old->obj.rolling_ball.vel.y * time + 0.5 * old->obj.rolling_ball.acc.y * time * time;
    // newRollingBall->obj.rolling_ball.pos.x = newX;
    // newRollingBall->obj.rolling_ball.pos.y = newY;
    new->obj.rolling_ball.pos.x = newX;
    new->obj.rolling_ball.pos.y = newY;
    //formula: vnew = vold + aold * time
    //Also had to check if velocity changed signs as well, if it did set acceleration and velocity of either the x or y componenet to 0.0
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    if(new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x < 0){
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;
    if(new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y < 0){
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
    //Setting new to new rolling ball then free newRollingBall
    // *new = *newRollingBall;

}
//Checking if a rolling ball has stopped
unsigned char phylib_stopped(phylib_object *object){
    int returnVal = 0;
    double check;
    phylib_coord c;
    //Needed to stop seg fault
    if(object == NULL){
        return 0;
    }
    //Checking if it is a rolling ball
    if(object->type != PHYLIB_ROLLING_BALL){
        return 0;
    }
    //Calculations to see if the ball stopped if less the epsilon convert to still ball and update still ball values coordinates and number
    c.x = object->obj.rolling_ball.vel.x;
    c.y = object->obj.rolling_ball.vel.y;
    check = phylib_length(c);
    if(check < PHYLIB_VEL_EPSILON){
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
        object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;
        returnVal = 1;
    }
    return returnVal;
}
//Bounce function
void phylib_bounce(phylib_object **a, phylib_object **b) {
    //Here so no seg fault occurs, and to make sure we dont access elements that are invalid
    if (*a == NULL || *b == NULL) {
        return;
    }
    if((*a)->type != PHYLIB_ROLLING_BALL){
        return;
    }
    //printf("BOUNCED \n");
    int check = (*b)->type;
    //Switch statement to apply bounce laws depending on what object b is
    switch (check) {
        case PHYLIB_HCUSHION:
            //If b is hcushion negate y vel and acc
            //printf("HIT 1\n");
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y * -1.0;
            (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y * -1.0;
            break;

        case PHYLIB_VCUSHION:
            //If b is a v cush negat x vel and acc
            //printf("HIT 2\n");
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x * -1.0;
            (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.acc.x * -1.0;
            break;

        case PHYLIB_HOLE:
            //If b is a hole, free a (the rolling ball) so it disappears to make it seem like it goes in the hole, set a to null as well.
            //printf("HIT 3\n");
            free(*a);
            *a = NULL;
            break;
        case PHYLIB_STILL_BALL:
            //If b is a still ball convert to rolling ball, but also update the number and intilize the new rolling ball velocties and acceleration so no nan or weird values occur
            //Also did not add a break statement so it goes to next case
            //printf("HIT 4\n");
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;
            (*b)->obj.rolling_ball.pos.x = (*b)->obj.still_ball.pos.x;
            (*b)->obj.rolling_ball.pos.y = (*b)->obj.still_ball.pos.y;
        case PHYLIB_ROLLING_BALL: {
            //If b is a rolling ball
            //printf("HIT 5\n");
            //Intializations made for intermeidate steps and calculation updates to the values
            phylib_coord r_ab, v_rel, n;
            double newX, newY;
            //Calculations of r_ab
            phylib_coord aPos = getRollingBallPos((*a)->obj.rolling_ball);
            phylib_coord bPos = getRollingBallPos((*b)->obj.rolling_ball);
            newX = aPos.x - bPos.x;
            newY = aPos.y - bPos.y;
            r_ab.x = newX;
            r_ab.y = newY;
            //Calculations of v_rel
            v_rel.x = (*a)->obj.rolling_ball.vel.x - (*b)->obj.rolling_ball.vel.x;
            v_rel.y = (*a)->obj.rolling_ball.vel.y - (*b)->obj.rolling_ball.vel.y;
            //getting length of r_ab so I can caluclate normal vector n
            double length_r_ab = phylib_length(r_ab);

            n.x = r_ab.x / length_r_ab;
            n.y = r_ab.y / length_r_ab;
            //V rel n calculation (dot product)
            double v_rel_n = phylib_dot_product(v_rel, n);
            // phylib_coord v_rel_n = phylib_subtract((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            //This is an extra intermidate step I did so I can update the a and b velocities
            double v_rel_n_x = v_rel_n * n.x;
            double v_rel_n_y = v_rel_n * n.y;

            (*a)->obj.rolling_ball.vel.x -= v_rel_n_x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n_y;

            (*b)->obj.rolling_ball.vel.x += v_rel_n_x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n_y;


            //Speed calculations
            double speedA = phylib_length((*a)->obj.rolling_ball.vel);
            double speedB = phylib_length((*b)->obj.rolling_ball.vel);

            //If speed greater the epsilon then update acceleration with these calculations (x and y)
            if (speedA > PHYLIB_VEL_EPSILON) {
                //Debug statements as acceleration was giving me some trouble
                //printf("Hit acc \n");
                //printf("SpeedA: %f, SpeedB: %f, PHYLIB_DRAG: %d\n", speedA, speedB, PHYLIB_DRAG);
                //printf("a: velx: %f vely %f \n", (*a)->obj.rolling_ball.vel.x, (*a)->obj.rolling_ball.vel.y);
                (*a)->obj.rolling_ball.acc.x = (-(*a)->obj.rolling_ball.vel.x / speedA) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = (-(*a)->obj.rolling_ball.vel.y / speedA) * PHYLIB_DRAG;
            }

            if (speedB > PHYLIB_VEL_EPSILON) {
                // printf("Hit acc 2\n");
                // printf("SpeedA: %f, SpeedB: %f, PHYLIB_DRAG: %d\n", speedA, speedB, PHYLIB_DRAG);
                // printf("b: velx: %f vely %f \n", (*b)->obj.rolling_ball.vel.x, (*b)->obj.rolling_ball.vel.y);
                (*b)->obj.rolling_ball.acc.x = (-(*b)->obj.rolling_ball.vel.x / speedB) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = (-(*b)->obj.rolling_ball.vel.y / speedB) * PHYLIB_DRAG;
            }

            break;
        }

    }
}


//Phylib Rolling function
unsigned char phylib_rolling(phylib_table *t){
    //Counts how many rolling balls are in the table (t)
    int i;
    unsigned char rollingBalls = 0;
    for(i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        //Had to check for null as it will give seg fault if you dont
        if(t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL){
            rollingBalls++;
        }
    }
    return rollingBalls;
}

phylib_table *phylib_segment(phylib_table *table){
    //Lots of debugging statements were needed here
    //printf("Check 3 \n");
    //Finding out how many rolling balls there are
    int rollingBalls = phylib_rolling(table);
    //Intialization of distance and setting time to PHYLIB_SIM_RATE
    double distance = 0.0;
    double time = PHYLIB_SIM_RATE;
    int i, j, check;
    check = 0;
    //Creating a copy table which is returned
    phylib_table * copyTable = phylib_copy_table(table);
    //printf("Check 4 \n");
    //phylib_object * copyObj = NULL;
    //If rolling balls is equal to zero then segment ends as it is done. Make sure to free the copyTable
    if(rollingBalls == 0){
        phylib_free_table(copyTable);
        return NULL;
    }
    //While loop to do the segment, will end if it goes over the max time
    while(time < PHYLIB_MAX_TIME){
        //iterating through the table object array (when rolling ball is found do this:)
        for(i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if(copyTable->object[i] != NULL && copyTable->object[i]->type == PHYLIB_ROLLING_BALL){
                //printf("Seg Check \n");
                //When rolling ball is found apply roll function to update the new using copyTable and using the old rolling ball from table and the time.
                phylib_roll(copyTable->object[i], table->object[i], time);
            //     //Inner nested for loop to check the distance of each object from the rolling ball in question, if distance is less then zero that means bounce function needs to be called
            //     for(j = 0; j < PHYLIB_MAX_OBJECTS; j++){
            //         if(copyTable->object[j] != NULL && i != j){
            //             distance = phylib_distance(copyTable->object[i], copyTable->object[j]);
            //             if(distance <= 0.0){
            //                 //Bounce needs to happen so call it. Then I also set my check variable to 1 as a way to indicate to end this segment
            //                 phylib_bounce(&copyTable->object[i], &copyTable->object[j]);
            //                 check = 1;
            //             }
            //         }
            //     }
            //     //printf("Seg Check 2 \n");
            //     //Another check to see if the rolling ball in question has stopped, if it did set the check variable to one.
            //     if(phylib_stopped(copyTable->object[i]) == 1){
            //         check = 1;
            //     }
            }
        }
        //Checking for bounce and stoppage of balls
        //printf("check \n");
        for(i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if(copyTable->object[i] != NULL && copyTable->object[i]->type == PHYLIB_ROLLING_BALL){
                for(j = 0; j < PHYLIB_MAX_OBJECTS; j++)
                    if(copyTable->object[j] != NULL && i != j){
                        distance = phylib_distance(copyTable->object[i], copyTable->object[j]);
                        if(distance <= 0.0){
                            //Bounce needs to happen so call it. Then I also set my check variable to 1 as a way to indicate to end this segment
                            phylib_bounce(&copyTable->object[i], &copyTable->object[j]);
                            copyTable->time += time;
                            return copyTable; // check = 1;
                        }
                    }
                if(phylib_stopped(copyTable->object[i]) == 1){
                    copyTable->time += time;
                    return copyTable;// check = 1;
                }
            }
        }
        //If check == 1 then end this segment but update time first, I had to update time like this for some reason as it was not updating properly in the other way.
        if(check == 1){
            //printf("Hit Checkpoint \n");
            //copyTable->time += time + table->time;
            copyTable->time += time;
            return copyTable;
        }
        //Incrementing time
        time += PHYLIB_SIM_RATE;
    }
    //If it reaches max time it exits while loop so just return it how it is and update time again
    //copyTable->time += time + table->time;
    copyTable->time += time;
    return copyTable;
}

//New Given Function:
char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type)
    {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
            break;
    }
    return string;
}
