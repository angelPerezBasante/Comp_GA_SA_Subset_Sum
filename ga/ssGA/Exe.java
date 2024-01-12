///////////////////////////////////////////////////////////////////////////////
///            Steady State Genetic Algorithm v1.0                          ///
///                by Enrique Alba, July 2000                               ///
///                                                                         ///
///   Executable: set parameters, problem, and execution details here       ///
///////////////////////////////////////////////////////////////////////////////

package ga.ssGA;

import java.util.Random;

public class Exe
{
  public static void main(String args[]) throws Exception
  {

    // PARAMETERS SUBSET_SUM - Se ha modificado para que gn, popsize, pc, pm y MAX_ISTEPS sean parámetros de entrada
    int gn            = Integer.valueOf(args[0]);    // Gene number
    int gl            = 1;               // Gene length
    int popsize           = Integer.valueOf(args[1]);    // Population size
    double pc                = Double.valueOf(args[2]); // Crossover probability
    double pm                = Double.valueOf(args[3]); // Mutation probability
    double tf         = (double)300500 ;      // Target fitness beign sought
    long evaluationCounterLimit = (long) Integer.valueOf(args[4]);    // Max number of evaluations
    long seed = (long) Integer.valueOf(args[5]);  //seed

/*
    // PARAMETERS PPEAKS
    int    gn         = 512;                           // Gene number
    int    gl         = 1;                            // Gene length
    int    popsize    = 512;                          // Population size
    double pc         = 0.8;                          // Crossover probability
    double pm  = 1.0/(double)((double)gn*(double)gl); // Mutation probability
    double tf         = (double)1 ;              // Target fitness beign sought
    long   MAX_ISTEPS = 50000;
*/

/*
    // PARAMETERS ONEMAX
    int    gn         = 512;                          // Gene number
    int    gl         = 1;                            // Gene length
    int    popsize    = 512;                          // Population size
    double pc         = 0.8;                          // Crossover probability
    double pm  = 1.0/(double)((double)gn*(double)gl); // Mutation probability
    double tf         = (double)gn*gl ;           // Target fitness being sought
    long   MAX_ISTEPS = 50000;
*/

    Random rWithSeed = new Random(seed); // Only the first time it is initialized with a specific seed

    Problem   problem;                             // The problem being solved

    problem = new ProblemPPeaks();
    // problem = new ProblemOneMax();
    
    problem.set_geneN(gn);
    problem.set_geneL(gl);
    problem.set_target_fitness(tf);
    //problem.set_rWithSeed(rWithSeed);



    Algorithm ga;          // The ssGA being used
    ga = new Algorithm(problem, popsize, gn, gl, pc, pm, rWithSeed); //The first initial population is generated and evaluated

    //Execute GA steps
    while (problem.get_fitness_counter()<evaluationCounterLimit)
    {
      ga.go_one_step();
      System.out.print(problem.get_fitness_counter()); System.out.print("  ");
      System.out.println(ga.get_bestf());

      //if(     (problem.tf_known())                    &&
      //(ga.get_solution()).get_fitness()>=problem.get_target_fitness())
      //{ //System.out.print("Solution Found! After ");
        //System.out.print(problem.get_fitness_counter());
        //System.out.println(" evaluations");
        //break;
      //}
    }

    // Print the solution
    //for(int i=0;i<gn*gl;i++)
      //System.out.print( (ga.get_solution()).get_allele(i) ); System.out.println();
    //System.out.println((ga.get_solution()).get_fitness());
  }

}
// END OF CLASS: Exe
