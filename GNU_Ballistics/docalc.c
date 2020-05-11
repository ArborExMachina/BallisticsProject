#include <stdio.h>
#include "ballistics.h"

enum Fields{
	BC, V, SH, ANGLE, WINDSPEED, WINDANGLE, ZERO, RANGESTART, RANGEEND, RESOLUTION
};

#define GetArg(arg) atof(argv[arg+1]) 

int main(int argc, char**argv){
	int k=0;
	double* sln;// A pointer for receiving the ballistic solution.
	// double bc=0.48; // The ballistic coefficient for the projectile.
	// double v=atof(argv[1]); // Intial velocity, in ft/s
	// double sh=1.5; // The Sight height over bore, in inches.
	// double angle=0; // The shooting angle (uphill / downhill), in degrees.
	// double zero=100; // The zero range of the rifle, in yards.
	// double windspeed=10; // The wind speed in miles per hour.
	// double windangle=90; // The wind angle (0=headwind, 90=right to left, 180=tailwind, 270/-90=left to right)
	
	double bc = atof(argv[BC+1]);
	double v = atof(argv[V+1]);
	double sh = atof(argv[SH+1]);
	double angle = atof(argv[ANGLE+1]);
	double windspeed = atof(argv[WINDSPEED+1]);
	double windangle = atof(argv[WINDANGLE+1]);
	double zero = atof(argv[ZERO+1]);
	int rangeStart = atoi(argv[RANGESTART + 1]);
	int rangeEnd = atoi(argv[RANGEEND + 1]);
	int resolution = atoi(argv[RESOLUTION + 1]);


	// TODO: Add params for max-range and measurment increment


	// If we wish to use the weather correction features, we need to 
	// Correct the BC for any weather conditions.  If we want standard conditions,
	// then we can just leave this commented out.
//  DragCoefficient,  Altitude,  Barometer,  Temperature, RelativeHumidity);
	// TODO: paramatize
	//bc=AtmCorrect(bc, 4500, 29.89, 59, 0.0078);
	
	
	// First find the angle of the bore relative to the sighting system.
	// We call this the "zero angle", since it is the angle required to 
	// achieve a zero at a particular yardage.  This value isn't very useful
	// to us, but is required for making a full ballistic solution.
	// It is left here to allow for zero-ing at altitudes (bc) different from the
	// final solution, or to allow for zero's other than 0" (ex: 3" high at 100 yds)
	double zeroangle=0;
	zeroangle=ZeroAngle(G1,bc,v,sh,zero,0);
	
	// Now we have everything needed to generate a full solution.
	// So we do.  The solution is stored in the pointer "sln" passed as the last argument.
	// k has the number of yards the solution is valid for, also the number of rows in the solution.
	k=SolveAll(G1,bc,v,sh,angle,zeroangle,windspeed,windangle,&sln);
	
	//Now print a simple chart of X / Y trajectory spaced at 10yd increments
	// TODO: All the things
	// printf("%.0f,%.2f",GetRange(sln,0), GetPath(sln,0));
	int s=0;
	for (s=rangeStart; s <= rangeEnd; s += resolution){
		printf("\n%.0f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f",
			GetRange(sln,s),
			GetPath(sln,s),
			GetMOA(sln, s),
			GetTime(sln, s),
			GetWindage(sln, s),
			GetWindageMOA(sln, s),
			GetVelocity(sln, s)
		);
	}
	
	// for(int i = 0; i < argc; i++)
	// {
	// 	printf("%s\n", argv[i]);
	// }
	
	return 0;
}

