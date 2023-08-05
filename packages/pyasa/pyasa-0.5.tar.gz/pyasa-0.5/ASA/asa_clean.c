/***********************************************************************
* Adaptive Simulated Annealing (ASA)
* Lester Ingber <ingber@ingber.com>
* Copyright (c) 1987-2012 Lester Ingber.  All Rights Reserved.
* The ASA-LICENSE file must be included with ASA code.
***********************************************************************/

#define ASA_ID "/* $Id: asa.c,v 28.12 2012/07/02 23:58:51 ingber Exp ingber $ */"

#include "asa.h"

char exit_msg[160];             /* temp storage for exit messages */

/***********************************************************************
* asa
*       This procedure implements the full ASA function optimization.
***********************************************************************/
double
asa (user_cost_function,
     user_random_generator,
     seed,
     parameter_initial_final,
     parameter_minimum,
     parameter_maximum,
     tangents,
     curvature,
     number_parameters,
     parameter_type, valid_state_generated_flag, exit_status, OPTIONS)
     double (*user_cost_function) ();
     double (*user_random_generator) ();
     LONG_INT *seed;
     double *parameter_initial_final;
     double *parameter_minimum;
     double *parameter_maximum;
     double *tangents;
     double *curvature;
     ALLOC_INT *number_parameters;
     int *parameter_type;
     int *valid_state_generated_flag;
     int *exit_status;
     USER_DEFINES *OPTIONS;
{
  int immediate_flag;           /* save Immediate_Exit */
  int index_cost_constraint;    /* index cost functions averaged */

  int index_cost_repeat,        /* test OPTIONS->Cost_Precision when =
                                   OPTIONS->Maximum_Cost_Repeat */
    tmp_var_int, tmp_var_int1, tmp_var_int2;    /* temporary integers */

  ALLOC_INT index_v,            /* iteration index */
   *start_sequence;             /* initial OPTIONS->Sequential_Parameters
                                   used if >= 0 */
  double final_cost,            /* best cost to return to user */
    tmp_var_db, tmp_var_db1, tmp_var_db2;       /* temporary doubles */
  int *curvature_flag;
  FILE *ptr_asa_out;            /* file ptr to output file */
  int ret1_flg;

  /* The 3 states that are kept track of during the annealing process */
  STATE *current_generated_state, *last_saved_state, *best_generated_state;




  int asa_exit_value;
  int best_flag;
  int fscanf_ret;

  double xnumber_parameters[1];

  /* The array of tangents (absolute value of the numerical derivatives),
     and the maximum |tangent| of the array */
  double *maximum_tangent;

  /* ratio of acceptances to generated points - determines when to
     test/reanneal */
  double *accepted_to_generated_ratio;

  /* temperature parameters */
  double temperature_scale, *temperature_scale_parameters;
  /* relative scalings of cost and parameters to temperature_scale */
  double *temperature_scale_cost;
  double *current_user_parameter_temp;
  double *initial_user_parameter_temp;
  double *current_cost_temperature;
  double *initial_cost_temperature;
  double log_new_temperature_ratio;     /* current *temp = initial *temp *
                                           exp(log_new_temperature_ratio) */
  ALLOC_INT *index_exit_v;      /* information for asa_exit */

  /* counts of generated states and acceptances */
  LONG_INT *index_parameter_generations;
  LONG_INT *number_generated, *best_number_generated_saved;
  LONG_INT *recent_number_generated, *number_accepted;
  LONG_INT *recent_number_acceptances, *index_cost_acceptances;
  LONG_INT *number_acceptances_saved, *best_number_accepted_saved;

  /* Flag indicates that the parameters generated were
     invalid according to the cost function validity criteria. */
  LONG_INT *number_invalid_generated_states;
  LONG_INT repeated_invalid_states;




  /* used to index repeated and recursive calls to asa */
  /* This assumes that multiple calls (>= 1) _or_ recursive
     calls are being made to asa */
  static int asa_open = FALSE;
  static int number_asa_open = 0;
  static int recursive_asa_open = 0;

  /* initializations */

  ret1_flg = 0;

  fscanf_ret = 0;               /* stop compiler warning */
  if (fscanf_ret) {
    ;
  }

  if ((curvature_flag = (int *) calloc (1, sizeof (int))) == NULL) {
    strcpy (exit_msg, "asa(): curvature_flag");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((maximum_tangent = (double *) calloc (1, sizeof (double))) == NULL) {
    strcpy (exit_msg, "asa(): maximum_tangent");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((accepted_to_generated_ratio =
       (double *) calloc (1, sizeof (double))) == NULL) {
    strcpy (exit_msg, "asa(): accepted_to_generated_ratio");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((temperature_scale_cost =
       (double *) calloc (1, sizeof (double))) == NULL) {
    strcpy (exit_msg, "asa(): temperature_scale_cost");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((current_cost_temperature =
       (double *) calloc (1, sizeof (double))) == NULL) {
    strcpy (exit_msg, "asa(): current_cost_temperature");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((initial_cost_temperature =
       (double *) calloc (1, sizeof (double))) == NULL) {
    strcpy (exit_msg, "asa(): initial_cost_temperature");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((index_exit_v = (ALLOC_INT *) calloc (1, sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): index_exit_v");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((start_sequence = (ALLOC_INT *) calloc (1, sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): start_sequence");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((number_generated =
       (ALLOC_INT *) calloc (1, sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): number_generated");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((best_number_generated_saved =
       (ALLOC_INT *) calloc (1, sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): best_number_generated_saved");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((recent_number_generated =
       (ALLOC_INT *) calloc (1, sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): recent_number_generated");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((number_accepted =
       (ALLOC_INT *) calloc (1, sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): number_accepted");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((recent_number_acceptances =
       (ALLOC_INT *) calloc (1, sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): recent_number_acceptances");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((index_cost_acceptances =
       (ALLOC_INT *) calloc (1, sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): index_cost_acceptances");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((number_acceptances_saved =
       (ALLOC_INT *) calloc (1, sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): number_acceptances_saved");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((best_number_accepted_saved =
       (ALLOC_INT *) calloc (1, sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): best_number_accepted_saved");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((number_invalid_generated_states =
       (ALLOC_INT *) calloc (1, sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): number_invalid_generated_states");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }

  if ((current_generated_state =
       (STATE *) calloc (1, sizeof (STATE))) == NULL) {
    strcpy (exit_msg, "asa(): current_generated_state");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((last_saved_state = (STATE *) calloc (1, sizeof (STATE))) == NULL) {
    strcpy (exit_msg, "asa(): last_saved_state");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }
  if ((best_generated_state = (STATE *) calloc (1, sizeof (STATE))) == NULL) {
    strcpy (exit_msg, "asa(): best_generated_state");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    return (-1);
  }

  fscanf_ret = 0;

  /* set default */
  ptr_asa_out = (FILE *) NULL;

  OPTIONS->Immediate_Exit = FALSE;

  if (asa_open == FALSE) {
    asa_open = TRUE;
    ++number_asa_open;
  } else {
    ++recursive_asa_open;
  }




  /* set indices and counts to 0 */
  *best_number_generated_saved =
    *number_generated =
    *recent_number_generated = *recent_number_acceptances = 0;
  *index_cost_acceptances =
    *best_number_accepted_saved =
    *number_accepted = *number_acceptances_saved = 0;
  index_cost_repeat = 0;

  OPTIONS->N_Accepted = *number_accepted;
  OPTIONS->N_Generated = *number_generated;


  /* do not calculate curvatures initially */
  *curvature_flag = FALSE;

  /* allocate storage for all parameters */
  if ((current_generated_state->parameter =
       (double *) calloc (*number_parameters, sizeof (double))) == NULL) {
    strcpy (exit_msg, "asa(): current_generated_state->parameter");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    ret1_flg = 1;
    goto RET1_asa;
  }
  if ((last_saved_state->parameter =
       (double *) calloc (*number_parameters, sizeof (double))) == NULL) {
    strcpy (exit_msg, "asa(): last_saved_state->parameter");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    ret1_flg = 1;
    goto RET1_asa;
  }
  if ((best_generated_state->parameter =
       (double *) calloc (*number_parameters, sizeof (double))) == NULL) {
    strcpy (exit_msg, "asa(): best_generated_state->parameter");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    ret1_flg = 1;
    goto RET1_asa;
  }

  OPTIONS->Best_Cost = &(best_generated_state->cost);
  OPTIONS->Best_Parameters = best_generated_state->parameter;
  OPTIONS->Last_Cost = &(last_saved_state->cost);
  OPTIONS->Last_Parameters = last_saved_state->parameter;

  if ((initial_user_parameter_temp =
       (double *) calloc (*number_parameters, sizeof (double))) == NULL) {
    strcpy (exit_msg, "asa(): initial_user_parameter_temp");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    ret1_flg = 1;
    goto RET1_asa;
  }
  if ((index_parameter_generations =
       (ALLOC_INT *) calloc (*number_parameters,
                             sizeof (ALLOC_INT))) == NULL) {
    strcpy (exit_msg, "asa(): index_parameter_generations");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    ret1_flg = 1;
    goto RET1_asa;
  }

  /* set all temperatures */
  if ((current_user_parameter_temp =
       (double *) calloc (*number_parameters, sizeof (double))) == NULL) {
    strcpy (exit_msg, "asa(): current_user_parameter_temp");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    ret1_flg = 1;
    goto RET1_asa;
  }
  VFOR (index_v)
    current_user_parameter_temp[index_v] =
    initial_user_parameter_temp[index_v] =
    OPTIONS->Initial_Parameter_Temperature;

  if ((temperature_scale_parameters =
       (double *) calloc (*number_parameters, sizeof (double))) == NULL) {
    strcpy (exit_msg, "asa(): temperature_scale_parameters");
    Exit_ASA (exit_msg);
    *exit_status = CALLOC_FAILED;
    ret1_flg = 1;
    goto RET1_asa;
  }

RET1_asa:
  if (ret1_flg == 1) {
    free (accepted_to_generated_ratio);
    free (best_generated_state);
    free (best_number_accepted_saved);
    free (best_number_generated_saved);
    free (current_cost_temperature);
    free (current_generated_state);
    free (curvature_flag);
    free (index_cost_acceptances);
    free (index_exit_v);
    free (initial_cost_temperature);
    free (last_saved_state);
    free (maximum_tangent);
    free (number_acceptances_saved);
    free (number_accepted);
    free (number_generated);
    free (number_invalid_generated_states);
    free (recent_number_acceptances);
    free (recent_number_generated);
    free (start_sequence);
    free (temperature_scale_cost);

    return (-1);
  }

  /* set parameters to the initial parameter values */
  VFOR (index_v)
    last_saved_state->parameter[index_v] =
    current_generated_state->parameter[index_v] =
    parameter_initial_final[index_v];


  /* save initial user value of OPTIONS->Sequential_Parameters */
  *start_sequence = OPTIONS->Sequential_Parameters;




  if (OPTIONS->Asa_Recursive_Level > asa_recursive_max)
    asa_recursive_max = OPTIONS->Asa_Recursive_Level;

  tmp_var_int = cost_function_test (current_generated_state->cost,
                                    current_generated_state->parameter,
                                    parameter_minimum,
                                    parameter_maximum, number_parameters,
                                    xnumber_parameters);

  /* compute temperature scales */
  tmp_var_db1 = -F_LOG ((OPTIONS->Temperature_Ratio_Scale));
  tmp_var_db2 = F_LOG (OPTIONS->Temperature_Anneal_Scale);
  temperature_scale =
    tmp_var_db1 * F_EXP (-tmp_var_db2 / *xnumber_parameters);

  /* set here in case not used */
  tmp_var_db = ZERO;

  VFOR (index_v)
    temperature_scale_parameters[index_v] =
    tmp_var_db1 * F_EXP (-(tmp_var_db2) / *xnumber_parameters);

    *temperature_scale_cost =
    tmp_var_db1 * F_EXP (-(tmp_var_db2)
                         / *xnumber_parameters) *
    OPTIONS->Cost_Parameter_Scale_Ratio;

  /* set the initial index of parameter generations to 1 */
  VFOR (index_v) index_parameter_generations[index_v] = 1;

  /* test user-defined options before calling cost function */
  tmp_var_int = asa_test_asa_options (seed,
                                      parameter_initial_final,
                                      parameter_minimum,
                                      parameter_maximum,
                                      tangents,
                                      curvature,
                                      number_parameters,
                                      parameter_type,
                                      valid_state_generated_flag,
                                      exit_status, ptr_asa_out, OPTIONS);
  if (tmp_var_int > 0) {
    *exit_status = INVALID_USER_INPUT;
    goto EXIT_asa;
  }
  /* calculate the average cost over samplings of the cost function */
  if (OPTIONS->Number_Cost_Samples < -1) {
    tmp_var_db1 = ZERO;
    tmp_var_db2 = ZERO;
    tmp_var_int = -OPTIONS->Number_Cost_Samples;
  } else {
    tmp_var_db1 = ZERO;
    tmp_var_int = OPTIONS->Number_Cost_Samples;
  }

  OPTIONS->Locate_Cost = 0;     /* initial cost temp */

  for (index_cost_constraint = 0;
       index_cost_constraint < tmp_var_int; ++index_cost_constraint) {
    *number_invalid_generated_states = 0;
    repeated_invalid_states = 0;
    OPTIONS->Sequential_Parameters = *start_sequence - 1;
    do {
      ++(*number_invalid_generated_states);
      generate_new_state (user_random_generator,
                          seed,
                          parameter_minimum,
                          parameter_maximum, current_user_parameter_temp,
                          number_parameters,
                          parameter_type,
                          current_generated_state, last_saved_state, OPTIONS);
      *valid_state_generated_flag = TRUE;
      tmp_var_db =
        user_cost_function (current_generated_state->parameter,
                            parameter_minimum,
                            parameter_maximum,
                            tangents,
                            curvature,
                            number_parameters,
                            parameter_type,
                            valid_state_generated_flag, exit_status, OPTIONS);
      if (cost_function_test
          (tmp_var_db, current_generated_state->parameter,
           parameter_minimum, parameter_maximum, number_parameters,
           xnumber_parameters) == 0) {
        *exit_status = INVALID_COST_FUNCTION;
        goto EXIT_asa;
      }

      ++repeated_invalid_states;
      if (repeated_invalid_states > OPTIONS->Limit_Invalid_Generated_States) {
        *exit_status = TOO_MANY_INVALID_STATES;
        goto EXIT_asa;
      }
    }
    while (*valid_state_generated_flag == FALSE);
    --(*number_invalid_generated_states);

    if (OPTIONS->Number_Cost_Samples < -1) {
      tmp_var_db1 += tmp_var_db;
      tmp_var_db2 += (tmp_var_db * tmp_var_db);
    } else {
      tmp_var_db1 += fabs (tmp_var_db);
    }
  }
  if (OPTIONS->Number_Cost_Samples < -1) {
    tmp_var_db1 /= (double) tmp_var_int;
    tmp_var_db2 /= (double) tmp_var_int;
    tmp_var_db = sqrt (fabs ((tmp_var_db2 - tmp_var_db1 * tmp_var_db1)
                             * ((double) tmp_var_int
                                / ((double) tmp_var_int - ONE))))
      + (double) EPS_DOUBLE;
  } else {
    tmp_var_db = tmp_var_db1 / (double) tmp_var_int;
  }

    *initial_cost_temperature = *current_cost_temperature = tmp_var_db;
  if (fabs (*initial_cost_temperature) <= SMALL_FLOAT) {
    *initial_cost_temperature = *current_cost_temperature = 2.718;
  }

  /* set all parameters to the initial parameter values */
  VFOR (index_v)
    best_generated_state->parameter[index_v] =
    last_saved_state->parameter[index_v] =
    current_generated_state->parameter[index_v] =
    parameter_initial_final[index_v];

  OPTIONS->Locate_Cost = 1;     /* initial cost value */

  /* if using user's initial parameters */
  if (OPTIONS->User_Initial_Parameters == TRUE) {
    *valid_state_generated_flag = TRUE;
      current_generated_state->cost =
        user_cost_function (current_generated_state->parameter,
                            parameter_minimum,
                            parameter_maximum,
                            tangents,
                            curvature,
                            number_parameters,
                            parameter_type,
                            valid_state_generated_flag, exit_status, OPTIONS);
    if (cost_function_test
        (current_generated_state->cost, current_generated_state->parameter,
         parameter_minimum, parameter_maximum, number_parameters,
         xnumber_parameters) == 0) {
      *exit_status = INVALID_COST_FUNCTION;
      goto EXIT_asa;
    }
  } else {
    /* let asa generate valid initial parameters */
    repeated_invalid_states = 0;
    OPTIONS->Sequential_Parameters = *start_sequence - 1;
    do {
      ++(*number_invalid_generated_states);
      generate_new_state (user_random_generator,
                          seed,
                          parameter_minimum,
                          parameter_maximum, current_user_parameter_temp,
                          number_parameters,
                          parameter_type,
                          current_generated_state, last_saved_state, OPTIONS);
      *valid_state_generated_flag = TRUE;
      current_generated_state->cost =
        user_cost_function (current_generated_state->parameter,
                            parameter_minimum,
                            parameter_maximum,
                            tangents,
                            curvature,
                            number_parameters,
                            parameter_type,
                            valid_state_generated_flag, exit_status, OPTIONS);
      if (cost_function_test
          (current_generated_state->cost,
           current_generated_state->parameter, parameter_minimum,
           parameter_maximum, number_parameters, xnumber_parameters) == 0) {
        *exit_status = INVALID_COST_FUNCTION;
        goto EXIT_asa;
      }
      ++repeated_invalid_states;
      if (repeated_invalid_states > OPTIONS->Limit_Invalid_Generated_States) {
        *exit_status = TOO_MANY_INVALID_STATES;
        goto EXIT_asa;
      }
    }
    while (*valid_state_generated_flag == FALSE);
    --(*number_invalid_generated_states);
  }                             /* OPTIONS->User_Initial_Parameters */

  /* set all states to the last one generated */
  VFOR (index_v) {
    best_generated_state->parameter[index_v] =
      last_saved_state->parameter[index_v] =
      current_generated_state->parameter[index_v];
  }

  /* set all costs to the last one generated */
  best_generated_state->cost = last_saved_state->cost =
    current_generated_state->cost;

  *accepted_to_generated_ratio = ONE;

  /* do not calculate curvatures initially */
  *curvature_flag = FALSE;



  /* reset the current cost and the number of generations performed */
  *number_invalid_generated_states = 0;
  *best_number_generated_saved =
    *number_generated = *recent_number_generated = 0;
  OPTIONS->N_Generated = *number_generated;
  VFOR (index_v) {
    /* ignore parameters that have too small a range */
    if (PARAMETER_RANGE_TOO_SMALL (index_v))
      continue;
    index_parameter_generations[index_v] = 1;
  }




  /* this test is after MULTI_MIN so that params are not all just set to 0 */
  if (*initial_cost_temperature < (double) EPS_DOUBLE) {
    *exit_status = INVALID_COST_FUNCTION;
    goto EXIT_asa;
  }

  OPTIONS->Sequential_Parameters = *start_sequence - 1;

  /* MAIN ANNEALING LOOP */
  while (((*number_accepted <= OPTIONS->Limit_Acceptances)
          || (OPTIONS->Limit_Acceptances == 0))
         && ((*number_generated <= OPTIONS->Limit_Generated)
             || (OPTIONS->Limit_Generated == 0))) {

    tmp_var_db1 = -F_LOG ((OPTIONS->Temperature_Ratio_Scale));

    /* compute temperature scales */
    tmp_var_db2 = F_LOG (OPTIONS->Temperature_Anneal_Scale);
    temperature_scale = tmp_var_db1 *
      F_EXP (-tmp_var_db2 / *xnumber_parameters);

    VFOR (index_v)
      temperature_scale_parameters[index_v] =
      tmp_var_db1 * F_EXP (-(tmp_var_db2) / *xnumber_parameters);

      *temperature_scale_cost =
      tmp_var_db1 * F_EXP (-(tmp_var_db2)
                           / *xnumber_parameters) *
      OPTIONS->Cost_Parameter_Scale_Ratio;

    /* CALCULATE NEW TEMPERATURES */

    /* calculate new parameter temperatures */
    VFOR (index_v) {
      /* skip parameters with too small a range */
      if (PARAMETER_RANGE_TOO_SMALL (index_v))
        continue;

      log_new_temperature_ratio =
        -temperature_scale_parameters[index_v] *
        F_POW ((double) index_parameter_generations[index_v],
               ONE
               / *xnumber_parameters);
      /* check (and correct) for too large an exponent */
      log_new_temperature_ratio = EXPONENT_CHECK (log_new_temperature_ratio);
      current_user_parameter_temp[index_v] =
        initial_user_parameter_temp[index_v]
        * F_EXP (log_new_temperature_ratio);

      /* check for too small a parameter temperature */
      if (current_user_parameter_temp[index_v] < (double) EPS_DOUBLE) {
        *exit_status = P_TEMP_TOO_SMALL;
        *index_exit_v = index_v;
        goto EXIT_asa;
      }
    }

    /* calculate new cost temperature */
    log_new_temperature_ratio =
      -*temperature_scale_cost * F_POW ((double) *index_cost_acceptances,
                                        ONE
                                        / *xnumber_parameters);
    log_new_temperature_ratio = EXPONENT_CHECK (log_new_temperature_ratio);
      *current_cost_temperature = *initial_cost_temperature
      * F_EXP (log_new_temperature_ratio);

    /* check for too small a cost temperature */
    if (*current_cost_temperature < (double) EPS_DOUBLE) {
      *exit_status = C_TEMP_TOO_SMALL;
      goto EXIT_asa;
    }


    /* GENERATE NEW PARAMETERS */

    /* generate a new valid set of parameters */

      if (OPTIONS->Locate_Cost < 0) {
        OPTIONS->Locate_Cost = 12;      /* generate new state from new best */
      } else {
        OPTIONS->Locate_Cost = 2;       /* generate new state */
      }

      repeated_invalid_states = 0;
      do {
        ++(*number_invalid_generated_states);
        generate_new_state (user_random_generator,
                            seed,
                            parameter_minimum,
                            parameter_maximum, current_user_parameter_temp,
                            number_parameters,
                            parameter_type,
                            current_generated_state,
                            last_saved_state, OPTIONS);

        *valid_state_generated_flag = TRUE;
        tmp_var_db =
          user_cost_function (current_generated_state->parameter,
                              parameter_minimum,
                              parameter_maximum,
                              tangents,
                              curvature,
                              number_parameters,
                              parameter_type,
                              valid_state_generated_flag,
                              exit_status, OPTIONS);
        if (cost_function_test (tmp_var_db,
                                current_generated_state->parameter,
                                parameter_minimum,
                                parameter_maximum, number_parameters,
                                xnumber_parameters) == 0) {
          *exit_status = INVALID_COST_FUNCTION;
          goto EXIT_asa;
        }
        current_generated_state->cost = tmp_var_db;
        ++repeated_invalid_states;
        if (repeated_invalid_states > OPTIONS->Limit_Invalid_Generated_States) {
          *exit_status = TOO_MANY_INVALID_STATES;
          goto EXIT_asa;
        }
      }
      while (*valid_state_generated_flag == FALSE);
      --(*number_invalid_generated_states);

    /* ACCEPT/REJECT NEW PARAMETERS */

      /* decide to accept/reject the new state */
      accept_new_state (user_random_generator,
                        seed,
                        parameter_minimum,
                        parameter_maximum, current_cost_temperature,
                        number_parameters,
                        recent_number_acceptances,
                        number_accepted,
                        index_cost_acceptances,
                        number_acceptances_saved,
                        recent_number_generated,
                        number_generated,
                        index_parameter_generations,
                        current_generated_state, last_saved_state,
                        OPTIONS);


      /* calculate the ratio of acceptances to generated states */
      *accepted_to_generated_ratio =
        (double) (*recent_number_acceptances + 1) /
        (double) (*recent_number_generated + 1);


      /* CHECK FOR NEW MINIMUM */

      if (current_generated_state->cost < best_generated_state->cost) {
        best_flag = 1;
      } else {
        best_flag = 0;
      }
      if (current_generated_state->cost < best_generated_state->cost)
      {
        /* NEW MINIMUM FOUND */

        OPTIONS->Locate_Cost = -1;

        /* reset the recent acceptances and generated counts */
        *recent_number_acceptances = *recent_number_generated = 0;
        if (best_flag == 1) {
          *best_number_generated_saved = *number_generated;
          *best_number_accepted_saved = *number_accepted;
        }
        index_cost_repeat = 0;

        /* copy the current state into the best_generated state */
        best_generated_state->cost = current_generated_state->cost;
        VFOR (index_v) {
          best_generated_state->parameter[index_v] =
            current_generated_state->parameter[index_v];
        }

        /* printout the new minimum state and value */

      }



    if (OPTIONS->Immediate_Exit == TRUE) {
      *exit_status = IMMEDIATE_EXIT;
      goto EXIT_asa;
    }

    /* PERIODIC TESTING/REANNEALING/PRINTING SECTION */

    if (OPTIONS->Acceptance_Frequency_Modulus == 0)
      tmp_var_int1 = FALSE;
    else if ((int) (*number_accepted %
                    ((LONG_INT) OPTIONS->Acceptance_Frequency_Modulus)) == 0
             && *number_acceptances_saved == *number_accepted)
      tmp_var_int1 = TRUE;
    else
      tmp_var_int1 = FALSE;

    if (OPTIONS->Generated_Frequency_Modulus == 0)
      tmp_var_int2 = FALSE;
    else if ((int) (*number_generated %
                    ((LONG_INT) OPTIONS->Generated_Frequency_Modulus)) == 0)
      tmp_var_int2 = TRUE;
    else
      tmp_var_int2 = FALSE;

    if (tmp_var_int1 == TRUE || tmp_var_int2 == TRUE
        || (*accepted_to_generated_ratio
            < OPTIONS->Accepted_To_Generated_Ratio)) {
      if (*accepted_to_generated_ratio
          < (OPTIONS->Accepted_To_Generated_Ratio))
        *recent_number_acceptances = *recent_number_generated = 0;

      /* if best.cost repeats OPTIONS->Maximum_Cost_Repeat then exit */
      if (OPTIONS->Maximum_Cost_Repeat != 0) {
        if (fabs (last_saved_state->cost - best_generated_state->cost)
            < OPTIONS->Cost_Precision) {
          ++index_cost_repeat;
          if (index_cost_repeat == (OPTIONS->Maximum_Cost_Repeat)) {
            *exit_status = COST_REPEATING;
            goto EXIT_asa;
          }
        } else {
          index_cost_repeat = 0;
        }
      }

      if (OPTIONS->Reanneal_Parameters == TRUE) {
        OPTIONS->Locate_Cost = 3;       /* reanneal parameters */

        /* calculate tangents, not curvatures, to reanneal */
        *curvature_flag = FALSE;
        cost_derivatives (user_cost_function,
                          parameter_minimum,
                          parameter_maximum,
                          tangents,
                          curvature,
                          maximum_tangent,
                          number_parameters,
                          parameter_type,
                          exit_status,
                          curvature_flag,
                          valid_state_generated_flag,
                          number_invalid_generated_states,
                          current_generated_state,
                          best_generated_state, ptr_asa_out, OPTIONS);
        if (*exit_status == INVALID_COST_FUNCTION_DERIV) {
          goto EXIT_asa;
        }
      }
      if (OPTIONS->Reanneal_Cost == 0 || OPTIONS->Reanneal_Cost == 1) {
        ;
      } else {
        immediate_flag = OPTIONS->Immediate_Exit;

        if (OPTIONS->Reanneal_Cost < -1) {
          tmp_var_int = -OPTIONS->Reanneal_Cost;
        } else {
          tmp_var_int = OPTIONS->Reanneal_Cost;
        }
        tmp_var_db1 = ZERO;
        tmp_var_db2 = ZERO;

        for (index_cost_constraint = 0;
             index_cost_constraint < tmp_var_int; ++index_cost_constraint) {
          OPTIONS->Locate_Cost = 4;     /* reanneal cost */

          *number_invalid_generated_states = 0;
          repeated_invalid_states = 0;
          OPTIONS->Sequential_Parameters = *start_sequence - 1;
          do {
            ++(*number_invalid_generated_states);
            generate_new_state (user_random_generator,
                                seed,
                                parameter_minimum,
                                parameter_maximum,
                                current_user_parameter_temp,
                                number_parameters,
                                parameter_type,
                                current_generated_state,
                                last_saved_state, OPTIONS);
            *valid_state_generated_flag = TRUE;

            tmp_var_db =
              user_cost_function (current_generated_state->parameter,
                                  parameter_minimum, parameter_maximum,
                                  tangents, curvature, number_parameters,
                                  parameter_type, valid_state_generated_flag,
                                  exit_status, OPTIONS);
            if (cost_function_test
                (tmp_var_db, current_generated_state->parameter,
                 parameter_minimum, parameter_maximum, number_parameters,
                 xnumber_parameters) == 0) {
              *exit_status = INVALID_COST_FUNCTION;
              goto EXIT_asa;
            }
            ++repeated_invalid_states;
            if (repeated_invalid_states >
                OPTIONS->Limit_Invalid_Generated_States) {
              *exit_status = TOO_MANY_INVALID_STATES;
              goto EXIT_asa;
            }
          }
          while (*valid_state_generated_flag == FALSE);
          --(*number_invalid_generated_states);

          tmp_var_db1 += tmp_var_db;
          tmp_var_db2 += (tmp_var_db * tmp_var_db);
        }
        tmp_var_db1 /= (double) tmp_var_int;
        tmp_var_db2 /= (double) tmp_var_int;
        tmp_var_db =
          sqrt (fabs
                ((tmp_var_db2 -
                  tmp_var_db1 * tmp_var_db1) * ((double) tmp_var_int /
                                                ((double) tmp_var_int -
                                                 ONE))));
        if (OPTIONS->Reanneal_Cost < -1) {
          *current_cost_temperature = *initial_cost_temperature =
            tmp_var_db + (double) EPS_DOUBLE;
        } else {
          *initial_cost_temperature = tmp_var_db + (double) EPS_DOUBLE;
        }
        OPTIONS->Immediate_Exit = immediate_flag;
      }

      reanneal (parameter_minimum,
                parameter_maximum,
                tangents,
                maximum_tangent,
                current_cost_temperature,
                initial_cost_temperature,
                temperature_scale_cost,
                current_user_parameter_temp,
                initial_user_parameter_temp,
                temperature_scale_parameters,
                number_parameters,
                parameter_type,
                index_cost_acceptances,
                index_parameter_generations,
                last_saved_state, best_generated_state, OPTIONS);
    }
  }

  /* FINISHED ANNEALING and MINIMIZATION */

  *exit_status = NORMAL_EXIT;
EXIT_asa:

  asa_exit_value = asa_exit (user_cost_function,
                             &final_cost,
                             parameter_initial_final,
                             parameter_minimum,
                             parameter_maximum,
                             tangents,
                             curvature,
                             maximum_tangent,
                             current_cost_temperature,
                             initial_user_parameter_temp,
                             current_user_parameter_temp,
                             accepted_to_generated_ratio,
                             number_parameters,
                             parameter_type,
                             valid_state_generated_flag,
                             exit_status,
                             index_exit_v,
                             start_sequence,
                             number_accepted,
                             best_number_accepted_saved,
                             index_cost_acceptances,
                             number_generated,
                             number_invalid_generated_states,
                             index_parameter_generations,
                             best_number_generated_saved,
                             current_generated_state,
                             last_saved_state,
                             best_generated_state, ptr_asa_out, OPTIONS);
  if (asa_exit_value == 9) {
    *exit_status = CALLOC_FAILED;
    return (-1);
  }

  free (curvature_flag);
  free (maximum_tangent);
  free (accepted_to_generated_ratio);
  free (temperature_scale_cost);
  free (current_cost_temperature);
  free (initial_cost_temperature);
  free (number_generated);
  free (best_number_generated_saved);
  free (recent_number_generated);
  free (number_accepted);
  free (recent_number_acceptances);
  free (index_cost_acceptances);
  free (number_acceptances_saved);
  free (best_number_accepted_saved);
  free (number_invalid_generated_states);
  free (current_generated_state->parameter);
  free (last_saved_state->parameter);
  free (best_generated_state->parameter);
  free (current_generated_state);
  free (last_saved_state);
  free (best_generated_state);
  free (initial_user_parameter_temp);
  free (index_exit_v);
  free (start_sequence);
  free (index_parameter_generations);
  free (current_user_parameter_temp);
  free (temperature_scale_parameters);
  if (recursive_asa_open == 0)
    asa_open = FALSE;
  return (final_cost);
}

/***********************************************************************
* asa_exit
*	This procedures copies the best parameters and cost into
*       final_cost and parameter_initial_final
***********************************************************************/
int

asa_exit (user_cost_function,
          final_cost,
          parameter_initial_final,
          parameter_minimum,
          parameter_maximum,
          tangents,
          curvature,
          maximum_tangent,
          current_cost_temperature,
          initial_user_parameter_temp,
          current_user_parameter_temp,
          accepted_to_generated_ratio,
          number_parameters,
          parameter_type,
          valid_state_generated_flag,
          exit_status,
          index_exit_v,
          start_sequence,
          number_accepted,
          best_number_accepted_saved,
          index_cost_acceptances,
          number_generated,
          number_invalid_generated_states,
          index_parameter_generations,
          best_number_generated_saved,
          current_generated_state,
          last_saved_state, best_generated_state, ptr_asa_out, OPTIONS)
     double (*user_cost_function) ();
     double *final_cost;
     double *parameter_initial_final;
     double *parameter_minimum;
     double *parameter_maximum;
     double *tangents;
     double *curvature;
     double *maximum_tangent;
     double *current_cost_temperature;
     double *initial_user_parameter_temp;
     double *current_user_parameter_temp;
     double *accepted_to_generated_ratio;
     ALLOC_INT *number_parameters;
     int *parameter_type;
     int *valid_state_generated_flag;
     int *exit_status;
     ALLOC_INT *index_exit_v;
     ALLOC_INT *start_sequence;
     LONG_INT *number_accepted;
     LONG_INT *best_number_accepted_saved;
     LONG_INT *index_cost_acceptances;
     LONG_INT *number_generated;
     LONG_INT *number_invalid_generated_states;
     LONG_INT *index_parameter_generations;
     LONG_INT *best_number_generated_saved;
     STATE *current_generated_state;
     STATE *last_saved_state;
     STATE *best_generated_state;
     FILE *ptr_asa_out;
     USER_DEFINES *OPTIONS;
{
  ALLOC_INT index_v;            /* iteration index */
  int curvatureFlag;
  int exit_exit_status, tmp_locate;

  tmp_locate = OPTIONS->Locate_Cost;
  if (tmp_locate) {             /* stop compiler warning */
    ;
  }

  exit_exit_status = 0;

  /* return final function minimum and associated parameters */
  *final_cost = best_generated_state->cost;
  VFOR (index_v) {
    parameter_initial_final[index_v] =
      best_generated_state->parameter[index_v];
  }

  OPTIONS->N_Accepted = *best_number_accepted_saved;
  OPTIONS->N_Generated = *best_number_generated_saved;

    if (*exit_status != TOO_MANY_INVALID_STATES
        && *exit_status != IMMEDIATE_EXIT
        && *exit_status != INVALID_USER_INPUT
        && *exit_status != INVALID_COST_FUNCTION
        && *exit_status != INVALID_COST_FUNCTION_DERIV) {
      if (OPTIONS->Curvature_0 != TRUE)
        OPTIONS->Locate_Cost = 5;       /* calc curvatures while exiting asa */

      /* calculate curvatures and tangents at best point */
      curvatureFlag = TRUE;
      cost_derivatives (user_cost_function,
                        parameter_minimum,
                        parameter_maximum,
                        tangents,
                        curvature,
                        maximum_tangent,
                        number_parameters,
                        parameter_type,
                        &exit_exit_status,
                        &curvatureFlag,
                        valid_state_generated_flag,
                        number_invalid_generated_states,
                        current_generated_state,
                        best_generated_state, ptr_asa_out, OPTIONS);
    }




  /* reset OPTIONS->Sequential_Parameters */
  OPTIONS->Sequential_Parameters = *start_sequence;


  return (0);
}

/***********************************************************************
* generate_new_state
*       Generates a valid new state from the old state
***********************************************************************/
void

generate_new_state (user_random_generator,
                    seed,
                    parameter_minimum,
                    parameter_maximum, current_user_parameter_temp,
                    number_parameters,
                    parameter_type,
                    current_generated_state, last_saved_state, OPTIONS)
     double (*user_random_generator) ();
     LONG_INT *seed;
     double *parameter_minimum;
     double *parameter_maximum;
     double *current_user_parameter_temp;
     ALLOC_INT *number_parameters;
     int *parameter_type;
     STATE *current_generated_state;
     STATE *last_saved_state;
     USER_DEFINES *OPTIONS;
{
  ALLOC_INT index_v;
  double x;
  double parameter_v, min_parameter_v, max_parameter_v, temperature_v,
    parameter_range_v;

  /* generate a new value for each parameter */
  VFOR (index_v) {
    if (OPTIONS->Sequential_Parameters >= -1) {
      ++OPTIONS->Sequential_Parameters;
      if (OPTIONS->Sequential_Parameters == *number_parameters)
        OPTIONS->Sequential_Parameters = 0;
      index_v = OPTIONS->Sequential_Parameters;
    }
    min_parameter_v = parameter_minimum[index_v];
    max_parameter_v = parameter_maximum[index_v];
    parameter_range_v = max_parameter_v - min_parameter_v;

    /* ignore parameters that have too small a range */
    if (fabs (parameter_range_v) < (double) EPS_DOUBLE)
      continue;

    temperature_v = current_user_parameter_temp[index_v];
    parameter_v = last_saved_state->parameter[index_v];

    /* Handle discrete parameters. */
    if (INTEGER_PARAMETER (index_v)) {
        min_parameter_v -= HALF;
        max_parameter_v += HALF;
        parameter_range_v = max_parameter_v - min_parameter_v;
      }

    /* generate a new state x within the parameter bounds */
    for (;;) {
      x = parameter_v
        + generate_asa_state (user_random_generator, seed, &temperature_v)
        * parameter_range_v;

      /* exit the loop if within its valid parameter range */
      if (x <= max_parameter_v - (double) EPS_DOUBLE
          && x >= min_parameter_v + (double) EPS_DOUBLE)
        break;
    }

    /* Handle discrete parameters.
       You might have to check rounding on your machine. */
    if (INTEGER_PARAMETER (index_v)) {
        if (x < min_parameter_v + HALF)
          x = min_parameter_v + HALF + (double) EPS_DOUBLE;
        if (x > max_parameter_v - HALF)
          x = max_parameter_v - HALF + (double) EPS_DOUBLE;

        if (x + HALF > ZERO) {
          x = (double) ((LONG_INT) (x + HALF));
        } else {
          x = (double) ((LONG_INT) (x - HALF));
        }
        if (x > parameter_maximum[index_v])
          x = parameter_maximum[index_v];
        if (x < parameter_minimum[index_v])
          x = parameter_minimum[index_v];
      }

    /* save the newly generated value */
    current_generated_state->parameter[index_v] = x;

    if (OPTIONS->Sequential_Parameters >= 0)
      break;
  }

}

/***********************************************************************
* generate_asa_state
*       This function generates a single value according to the
*       ASA generating function and the passed temperature
***********************************************************************/
double
generate_asa_state (user_random_generator, seed, temp)
     double (*user_random_generator) ();
     LONG_INT *seed;
     double *temp;
{
  double x, y, z;

  x = (*user_random_generator) (seed);
  y = x < HALF ? -ONE : ONE;
  z = y * *temp * (F_POW ((ONE + ONE / *temp), fabs (TWO * x - ONE)) - ONE);

  return (z);

}

/***********************************************************************
* accept_new_state
*	This procedure accepts or rejects a newly generated state,
*	depending on whether the difference between new and old
*	cost functions passes a statistical test. If accepted,
*	the current state is updated.
***********************************************************************/
void

accept_new_state (user_random_generator,
                  seed,
                  parameter_minimum,
                  parameter_maximum, current_cost_temperature,
                  number_parameters,
                  recent_number_acceptances,
                  number_accepted,
                  index_cost_acceptances,
                  number_acceptances_saved,
                  recent_number_generated,
                  number_generated,
                  index_parameter_generations,
                  current_generated_state, last_saved_state,
                  OPTIONS)
     double (*user_random_generator) ();
     LONG_INT *seed;
     double *parameter_minimum;
     double *parameter_maximum;
     double *current_cost_temperature;
     ALLOC_INT *number_parameters;
     LONG_INT *recent_number_acceptances;
     LONG_INT *number_accepted;
     LONG_INT *index_cost_acceptances;
     LONG_INT *number_acceptances_saved;
     LONG_INT *recent_number_generated;
     LONG_INT *number_generated;
     LONG_INT *index_parameter_generations;
     STATE *current_generated_state;
     STATE *last_saved_state;
     USER_DEFINES *OPTIONS;

{
  double delta_cost;
  double prob_test, unif_test;
  double curr_cost_temp;
  ALLOC_INT index_v;

  /* update accepted and generated count */
  ++*number_acceptances_saved;
  ++*recent_number_generated;
  ++*number_generated;
  OPTIONS->N_Generated = *number_generated;

  /* increment the parameter index generation for each parameter */
  if (OPTIONS->Sequential_Parameters >= 0) {
    /* ignore parameters with too small a range */
    if (!PARAMETER_RANGE_TOO_SMALL (OPTIONS->Sequential_Parameters))
      ++index_parameter_generations[OPTIONS->Sequential_Parameters];
  } else {
    VFOR (index_v) {
      if (!PARAMETER_RANGE_TOO_SMALL (index_v))
        ++index_parameter_generations[index_v];
    }
  }

  /* effective cost function for testing acceptance criteria,
     calculate the cost difference and divide by the temperature */
  curr_cost_temp = *current_cost_temperature;

  delta_cost = (current_generated_state->cost - last_saved_state->cost)
    / (curr_cost_temp + (double) EPS_DOUBLE);


  prob_test = MIN (ONE, (F_EXP (EXPONENT_CHECK (-delta_cost))));


  unif_test = (*user_random_generator) (seed);


  /* accept/reject the new state */
  if (prob_test >= unif_test) {
    /* copy current state to the last saved state */

    last_saved_state->cost = current_generated_state->cost;
    VFOR (index_v) {
      /* ignore parameters with too small a range */
      if (PARAMETER_RANGE_TOO_SMALL (index_v))
        continue;
      last_saved_state->parameter[index_v] =
        current_generated_state->parameter[index_v];
    }

    /* update acceptance counts */
    ++*recent_number_acceptances;
    ++*number_accepted;
    ++*index_cost_acceptances;
    *number_acceptances_saved = *number_accepted;
    OPTIONS->N_Accepted = *number_accepted;
  }
}

/***********************************************************************
* reanneal
*	Readjust temperatures of generating and acceptance functions
***********************************************************************/
void

reanneal (parameter_minimum,
          parameter_maximum,
          tangents,
          maximum_tangent,
          current_cost_temperature,
          initial_cost_temperature,
          temperature_scale_cost,
          current_user_parameter_temp,
          initial_user_parameter_temp,
          temperature_scale_parameters,
          number_parameters,
          parameter_type,
          index_cost_acceptances,
          index_parameter_generations,
          last_saved_state, best_generated_state, OPTIONS)
     double *parameter_minimum;
     double *parameter_maximum;
     double *tangents;
     double *maximum_tangent;
     double *current_cost_temperature;
     double *initial_cost_temperature;
     double *temperature_scale_cost;
     double *current_user_parameter_temp;
     double *initial_user_parameter_temp;
     double *temperature_scale_parameters;
     ALLOC_INT *number_parameters;
     int *parameter_type;
     LONG_INT *index_cost_acceptances;
     LONG_INT *index_parameter_generations;
     STATE *last_saved_state;
     STATE *best_generated_state;
     USER_DEFINES *OPTIONS;
{
  ALLOC_INT index_v;
  int cost_test;
  double tmp_var_db3;
  double new_temperature;
  double log_new_temperature_ratio;
  double log_init_cur_temp_ratio;
  double temperature_rescale_power;
  double cost_best, cost_last;
  double tmp_dbl, tmp_dbl1;

  double xnumber_parameters[1];

  cost_test = cost_function_test (last_saved_state->cost,
                                  last_saved_state->parameter,
                                  parameter_minimum,
                                  parameter_maximum, number_parameters,
                                  xnumber_parameters);

  if (OPTIONS->Reanneal_Parameters == TRUE) {
    VFOR (index_v) {
      if (NO_REANNEAL (index_v))
        continue;

      /* use the temp double to prevent overflow */
      tmp_dbl = (double) index_parameter_generations[index_v];

      /* skip parameters with too small range or integer parameters */
      if (OPTIONS->Include_Integer_Parameters == TRUE) {
        if (PARAMETER_RANGE_TOO_SMALL (index_v))
          continue;
      } else {
        if (PARAMETER_RANGE_TOO_SMALL (index_v) ||
            INTEGER_PARAMETER (index_v))
          continue;
      }

      /* ignore parameters with too small tangents */
      if (fabs (tangents[index_v]) < (double) EPS_DOUBLE)
        continue;

      /* reset the index of parameter generations appropriately */
      new_temperature =
        fabs (FUNCTION_REANNEAL_PARAMS
              (current_user_parameter_temp[index_v], tangents[index_v],
               *maximum_tangent));
      if (new_temperature < initial_user_parameter_temp[index_v]) {
        log_init_cur_temp_ratio =
          fabs (F_LOG (((double) EPS_DOUBLE
                        + initial_user_parameter_temp[index_v])
                       / ((double) EPS_DOUBLE + new_temperature)));
        tmp_dbl = (double) EPS_DOUBLE
          + F_POW (log_init_cur_temp_ratio
                   / temperature_scale_parameters[index_v],
                   *xnumber_parameters
          );
      } else {
        tmp_dbl = ONE;
      }

      /* Reset index_parameter_generations if index reset too large,
         and also reset the initial_user_parameter_temp, to achieve
         the same new temperature. */
      while (tmp_dbl > ((double) MAXIMUM_REANNEAL_INDEX)) {
        log_new_temperature_ratio =
          -temperature_scale_parameters[index_v] * F_POW (tmp_dbl,
                                                          ONE
                                                          /
                                                          *xnumber_parameters);
        log_new_temperature_ratio =
          EXPONENT_CHECK (log_new_temperature_ratio);
        new_temperature =
          initial_user_parameter_temp[index_v] *
          F_EXP (log_new_temperature_ratio);
        tmp_dbl /= (double) REANNEAL_SCALE;
        temperature_rescale_power = ONE / F_POW ((double) REANNEAL_SCALE,
                                                 ONE
                                                 / *xnumber_parameters);
        initial_user_parameter_temp[index_v] =
          new_temperature * F_POW (initial_user_parameter_temp[index_v] /
                                   new_temperature,
                                   temperature_rescale_power);
      }
      /* restore from temporary double */
      index_parameter_generations[index_v] = (LONG_INT) tmp_dbl;
    }
  }

  if (OPTIONS->Reanneal_Cost == 0) {
    ;
  } else if (OPTIONS->Reanneal_Cost < -1) {
    *index_cost_acceptances = 1;
  } else {
    /* reanneal : Reset the current cost temp and rescale the
       index of cost acceptances. */

    cost_best = best_generated_state->cost;
    cost_last = last_saved_state->cost;
    cost_test = TRUE;
    if (OPTIONS->Reanneal_Cost == 1) {
      /* (re)set the initial cost_temperature */
      tmp_dbl = MAX (fabs (cost_last), fabs (cost_best));
      tmp_dbl = MAX (tmp_dbl, fabs (cost_best - cost_last));
      tmp_dbl = MAX ((double) EPS_DOUBLE, tmp_dbl);
      *initial_cost_temperature = MIN (*initial_cost_temperature, tmp_dbl);
    }

    tmp_dbl = (double) *index_cost_acceptances;

    tmp_dbl1 = MAX (fabs (cost_last - cost_best), *current_cost_temperature);
    tmp_dbl1 = MAX ((double) EPS_DOUBLE, tmp_dbl1);
    tmp_dbl1 = MIN (tmp_dbl1, *initial_cost_temperature);
    if (cost_test == TRUE && (*current_cost_temperature > tmp_dbl1)) {
      tmp_var_db3 =
        fabs (F_LOG (((double) EPS_DOUBLE + *initial_cost_temperature) /
                     (tmp_dbl1)));
      tmp_dbl = (double) EPS_DOUBLE + F_POW (tmp_var_db3
                                             / *temperature_scale_cost,
                                             *xnumber_parameters
        );
    } else {
      log_init_cur_temp_ratio =
        fabs (F_LOG (((double) EPS_DOUBLE + *initial_cost_temperature) /
                     ((double) EPS_DOUBLE + *current_cost_temperature)));
      tmp_dbl = (double) EPS_DOUBLE
        + F_POW (log_init_cur_temp_ratio
                 / *temperature_scale_cost, *xnumber_parameters
        );
    }

    /* reset index_cost_temperature if index reset too large */
    while (tmp_dbl > ((double) MAXIMUM_REANNEAL_INDEX)) {
      log_new_temperature_ratio = -*temperature_scale_cost * F_POW (tmp_dbl,
                                                                    ONE
                                                                    /
                                                                    *xnumber_parameters);
      log_new_temperature_ratio = EXPONENT_CHECK (log_new_temperature_ratio);
      new_temperature =
        *initial_cost_temperature * F_EXP (log_new_temperature_ratio);
      tmp_dbl /= (double) REANNEAL_SCALE;
      temperature_rescale_power = ONE / F_POW ((double) REANNEAL_SCALE,
                                               ONE
                                               / *xnumber_parameters);
      *initial_cost_temperature =
        new_temperature * F_POW (*initial_cost_temperature /
                                 new_temperature, temperature_rescale_power);
    }
    *index_cost_acceptances = (LONG_INT) tmp_dbl;
  }
}

/***********************************************************************
* cost_derivatives
*	This procedure calculates the derivatives of the cost function
*	with respect to its parameters.  The first derivatives are
*	used as a sensitivity measure for reannealing.  The second
*	derivatives are calculated only if *curvature_flag=TRUE;
*	these are a measure of the covariance of the fit when a
*	minimum is found.
***********************************************************************/
  /* Calculate the numerical derivatives of the best
     generated state found so far */

  /* Assuming no information is given about the metric of the parameter
     space, use simple Cartesian space to calculate curvatures. */

void

cost_derivatives (user_cost_function,
                  parameter_minimum,
                  parameter_maximum,
                  tangents,
                  curvature,
                  maximum_tangent,
                  number_parameters,
                  parameter_type,
                  exit_status,
                  curvature_flag,
                  valid_state_generated_flag,
                  number_invalid_generated_states,
                  current_generated_state,
                  best_generated_state, ptr_asa_out, OPTIONS)
     double (*user_cost_function) ();
     double *parameter_minimum;
     double *parameter_maximum;
     double *tangents;
     double *curvature;
     double *maximum_tangent;
     ALLOC_INT *number_parameters;
     int *parameter_type;
     int *exit_status;
     int *curvature_flag;
     int *valid_state_generated_flag;
     LONG_INT *number_invalid_generated_states;
     STATE *current_generated_state;
     STATE *best_generated_state;
     FILE *ptr_asa_out;
     USER_DEFINES *OPTIONS;
{
  ALLOC_INT index_v, index_vv, index_v_vv, index_vv_v;
  LONG_INT saved_num_invalid_gen_states;
  double parameter_v, parameter_vv, parameter_v_offset, parameter_vv_offset;
  double recent_best_cost;
  double new_cost_state_1, new_cost_state_2, new_cost_state_3;
  double delta_parameter_v, delta_parameter_vv;
  int immediate_flag;

  if (OPTIONS->Curvature_0 == TRUE)
    *curvature_flag = FALSE;
  if (OPTIONS->Curvature_0 == -1)
    *curvature_flag = TRUE;

  /* save Immediate_Exit flag */
  immediate_flag = OPTIONS->Immediate_Exit;

  /* save the best cost */
  recent_best_cost = best_generated_state->cost;

  /* copy the best state into the current state */
  VFOR (index_v) {
    /* ignore parameters with too small ranges */
    if (PARAMETER_RANGE_TOO_SMALL (index_v))
      continue;
    current_generated_state->parameter[index_v] =
      best_generated_state->parameter[index_v];
  }

  saved_num_invalid_gen_states = (*number_invalid_generated_states);

  /* set parameters (& possibly constraints) to best state */
  *valid_state_generated_flag = TRUE;
  current_generated_state->cost =
    user_cost_function (current_generated_state->parameter,
                        parameter_minimum,
                        parameter_maximum,
                        tangents,
                        curvature,
                        number_parameters,
                        parameter_type,
                        valid_state_generated_flag, exit_status, OPTIONS);
  if ((*valid_state_generated_flag == FALSE)
      || ((current_generated_state->cost) != (current_generated_state->cost))
      || current_generated_state->cost < -MAX_DOUBLE
      || current_generated_state->cost > MAX_DOUBLE) {
    *exit_status = INVALID_COST_FUNCTION_DERIV;
    return;
  }
  if (*valid_state_generated_flag == FALSE)
    ++(*number_invalid_generated_states);

  if (OPTIONS->User_Tangents == TRUE) {
    *valid_state_generated_flag = FALSE;
    current_generated_state->cost =
      user_cost_function (current_generated_state->parameter,
                          parameter_minimum,
                          parameter_maximum,
                          tangents,
                          curvature,
                          number_parameters,
                          parameter_type,
                          valid_state_generated_flag, exit_status, OPTIONS);
    if ((*valid_state_generated_flag == FALSE)
        || ((current_generated_state->cost) !=
            (current_generated_state->cost))
        || current_generated_state->cost < -MAX_DOUBLE
        || current_generated_state->cost > MAX_DOUBLE) {
      *exit_status = INVALID_COST_FUNCTION_DERIV;
      return;
    }
    if (*valid_state_generated_flag == FALSE)
      ++(*number_invalid_generated_states);
  } else {
    /* calculate tangents */
    VFOR (index_v) {
      if (NO_REANNEAL (index_v)) {
        tangents[index_v] = ZERO;
        continue;
      }
      /* skip parameters with too small range or integer parameters */
      if (OPTIONS->Include_Integer_Parameters == TRUE) {
        if (PARAMETER_RANGE_TOO_SMALL (index_v)) {
          tangents[index_v] = ZERO;
          continue;
        }
      } else {
        if (PARAMETER_RANGE_TOO_SMALL (index_v) ||
            INTEGER_PARAMETER (index_v)) {
          tangents[index_v] = ZERO;
          continue;
        }
      }
      delta_parameter_v = OPTIONS->Delta_X;
      if (delta_parameter_v < SMALL_FLOAT) {
        tangents[index_v] = 0;
        continue;
      }

      /* save the v_th parameter and delta_parameter */
      parameter_v = best_generated_state->parameter[index_v];

      parameter_v_offset = (ONE + delta_parameter_v) * parameter_v;
      if (parameter_v_offset > parameter_maximum[index_v] ||
          parameter_v_offset < parameter_minimum[index_v]) {
        delta_parameter_v = -delta_parameter_v;
        parameter_v_offset = (ONE + delta_parameter_v) * parameter_v;
      }

      /* generate the first sample point */
      current_generated_state->parameter[index_v] = parameter_v_offset;
      *valid_state_generated_flag = TRUE;
      current_generated_state->cost =
        user_cost_function (current_generated_state->parameter,
                            parameter_minimum,
                            parameter_maximum,
                            tangents,
                            curvature,
                            number_parameters,
                            parameter_type,
                            valid_state_generated_flag, exit_status, OPTIONS);
      if ((*valid_state_generated_flag == FALSE)
          || ((current_generated_state->cost) !=
              (current_generated_state->cost))
          || current_generated_state->cost < -MAX_DOUBLE
          || current_generated_state->cost > MAX_DOUBLE) {
        *exit_status = INVALID_COST_FUNCTION_DERIV;
        return;
      }
      if (*valid_state_generated_flag == FALSE)
        ++(*number_invalid_generated_states);
      new_cost_state_1 = current_generated_state->cost;

      /* restore the parameter state */
      current_generated_state->parameter[index_v] = parameter_v;

      /* calculate the numerical derivative */
      tangents[index_v] = (new_cost_state_1 - recent_best_cost)
        / (delta_parameter_v * parameter_v + (double) EPS_DOUBLE);

    }
  }

  /* find the maximum |tangent| from all tangents */
  *maximum_tangent = 0;
  VFOR (index_v) {
    if (NO_REANNEAL (index_v))
      continue;

    /* ignore too small ranges and integer parameters types */
    if (OPTIONS->Include_Integer_Parameters == TRUE) {
      if (PARAMETER_RANGE_TOO_SMALL (index_v))
        continue;
    } else {
      if (PARAMETER_RANGE_TOO_SMALL (index_v)
          || INTEGER_PARAMETER (index_v))
        continue;
    }

    /* find the maximum |tangent| (from all tangents) */
    if (fabs (tangents[index_v]) > *maximum_tangent) {
      *maximum_tangent = fabs (tangents[index_v]);
    }
  }

  if (*curvature_flag == TRUE || *curvature_flag == -1) {
    /* calculate diagonal curvatures */
    VFOR (index_v) {
      /* index_v_vv: row index_v, column index_v */
      index_v_vv = ROW_COL_INDEX (index_v, index_v);

      if (NO_REANNEAL (index_v)) {
        curvature[index_v_vv] = ZERO;
        continue;
      }
      /* skip parameters with too small range or integer parameters */
      if (OPTIONS->Include_Integer_Parameters == TRUE) {
        if (PARAMETER_RANGE_TOO_SMALL (index_v)) {
          curvature[index_v_vv] = ZERO;
          continue;
        }
      } else {
        if (PARAMETER_RANGE_TOO_SMALL (index_v) ||
            INTEGER_PARAMETER (index_v)) {
          curvature[index_v_vv] = ZERO;
          continue;
        }
      }
      delta_parameter_v = OPTIONS->Delta_X;
      if (delta_parameter_v < SMALL_FLOAT) {
        curvature[index_v_vv] = ZERO;
        continue;
      }

      /* save the v_th parameter and delta_parameter */
      parameter_v = best_generated_state->parameter[index_v];

      if (parameter_v + delta_parameter_v * fabs (parameter_v)
          > parameter_maximum[index_v]) {
        /* generate the first sample point */
        current_generated_state->parameter[index_v] =
          parameter_v - TWO * delta_parameter_v * fabs (parameter_v);
        *valid_state_generated_flag = TRUE;
        current_generated_state->cost =
          user_cost_function (current_generated_state->parameter,
                              parameter_minimum,
                              parameter_maximum,
                              tangents,
                              curvature,
                              number_parameters,
                              parameter_type,
                              valid_state_generated_flag,
                              exit_status, OPTIONS);
        if ((*valid_state_generated_flag == FALSE)
            || ((current_generated_state->cost) !=
                (current_generated_state->cost))
            || current_generated_state->cost < -MAX_DOUBLE
            || current_generated_state->cost > MAX_DOUBLE) {
          *exit_status = INVALID_COST_FUNCTION_DERIV;
          return;
        }
        if (*valid_state_generated_flag == FALSE)
          ++(*number_invalid_generated_states);
        new_cost_state_1 = current_generated_state->cost;

        /* generate the second sample point */
        current_generated_state->parameter[index_v] =
          parameter_v - delta_parameter_v * fabs (parameter_v);

        *valid_state_generated_flag = TRUE;
        current_generated_state->cost =
          user_cost_function (current_generated_state->parameter,
                              parameter_minimum,
                              parameter_maximum,
                              tangents,
                              curvature,
                              number_parameters,
                              parameter_type,
                              valid_state_generated_flag,
                              exit_status, OPTIONS);
        if ((*valid_state_generated_flag == FALSE)
            || ((current_generated_state->cost) !=
                (current_generated_state->cost))
            || current_generated_state->cost < -MAX_DOUBLE
            || current_generated_state->cost > MAX_DOUBLE) {
          *exit_status = INVALID_COST_FUNCTION_DERIV;
          return;
        }
        if (*valid_state_generated_flag == FALSE)
          ++(*number_invalid_generated_states);
        new_cost_state_2 = current_generated_state->cost;

        /* restore the parameter state */
        current_generated_state->parameter[index_v] = parameter_v;

        /* calculate and store the curvature */
        curvature[index_v_vv] =
          (recent_best_cost - TWO * new_cost_state_2
           + new_cost_state_1) / (delta_parameter_v * delta_parameter_v
                                  * parameter_v * parameter_v +
                                  (double) EPS_DOUBLE);
      } else if (parameter_v - delta_parameter_v * fabs (parameter_v)
                 < parameter_minimum[index_v]) {
        /* generate the first sample point */
        current_generated_state->parameter[index_v] =
          parameter_v + TWO * delta_parameter_v * fabs (parameter_v);
        *valid_state_generated_flag = TRUE;
        current_generated_state->cost =
          user_cost_function (current_generated_state->parameter,
                              parameter_minimum,
                              parameter_maximum,
                              tangents,
                              curvature,
                              number_parameters,
                              parameter_type,
                              valid_state_generated_flag,
                              exit_status, OPTIONS);
        if ((*valid_state_generated_flag == FALSE)
            || ((current_generated_state->cost) !=
                (current_generated_state->cost))
            || current_generated_state->cost < -MAX_DOUBLE
            || current_generated_state->cost > MAX_DOUBLE) {
          *exit_status = INVALID_COST_FUNCTION_DERIV;
          return;
        }
        if (*valid_state_generated_flag == FALSE)
          ++(*number_invalid_generated_states);
        new_cost_state_1 = current_generated_state->cost;

        /* generate the second sample point */
        current_generated_state->parameter[index_v] =
          parameter_v + delta_parameter_v * fabs (parameter_v);

        *valid_state_generated_flag = TRUE;
        current_generated_state->cost =
          user_cost_function (current_generated_state->parameter,
                              parameter_minimum,
                              parameter_maximum,
                              tangents,
                              curvature,
                              number_parameters,
                              parameter_type,
                              valid_state_generated_flag,
                              exit_status, OPTIONS);
        if ((*valid_state_generated_flag == FALSE)
            || ((current_generated_state->cost) !=
                (current_generated_state->cost))
            || current_generated_state->cost < -MAX_DOUBLE
            || current_generated_state->cost > MAX_DOUBLE) {
          *exit_status = INVALID_COST_FUNCTION_DERIV;
          return;
        }
        if (*valid_state_generated_flag == FALSE)
          ++(*number_invalid_generated_states);
        new_cost_state_2 = current_generated_state->cost;

        /* restore the parameter state */
        current_generated_state->parameter[index_v] = parameter_v;

        /* index_v_vv: row index_v, column index_v */
        index_v_vv = ROW_COL_INDEX (index_v, index_v);

        /* calculate and store the curvature */
        curvature[index_v_vv] =
          (recent_best_cost - TWO * new_cost_state_2
           + new_cost_state_1) / (delta_parameter_v * delta_parameter_v
                                  * parameter_v * parameter_v +
                                  (double) EPS_DOUBLE);
      } else {
        /* generate the first sample point */
        parameter_v_offset = (ONE + delta_parameter_v) * parameter_v;
        current_generated_state->parameter[index_v] = parameter_v_offset;
        *valid_state_generated_flag = TRUE;
        current_generated_state->cost =
          user_cost_function (current_generated_state->parameter,
                              parameter_minimum,
                              parameter_maximum,
                              tangents,
                              curvature,
                              number_parameters,
                              parameter_type,
                              valid_state_generated_flag,
                              exit_status, OPTIONS);
        if ((*valid_state_generated_flag == FALSE)
            || ((current_generated_state->cost) !=
                (current_generated_state->cost))
            || current_generated_state->cost < -MAX_DOUBLE
            || current_generated_state->cost > MAX_DOUBLE) {
          *exit_status = INVALID_COST_FUNCTION_DERIV;
          return;
        }
        if (*valid_state_generated_flag == FALSE)
          ++(*number_invalid_generated_states);
        new_cost_state_1 = current_generated_state->cost;

        /* generate the second sample point */
        current_generated_state->parameter[index_v] =
          (ONE - delta_parameter_v) * parameter_v;

        *valid_state_generated_flag = TRUE;
        current_generated_state->cost =
          user_cost_function (current_generated_state->parameter,
                              parameter_minimum,
                              parameter_maximum,
                              tangents,
                              curvature,
                              number_parameters,
                              parameter_type,
                              valid_state_generated_flag,
                              exit_status, OPTIONS);
        if ((*valid_state_generated_flag == FALSE)
            || ((current_generated_state->cost) !=
                (current_generated_state->cost))
            || current_generated_state->cost < -MAX_DOUBLE
            || current_generated_state->cost > MAX_DOUBLE) {
          *exit_status = INVALID_COST_FUNCTION_DERIV;
          return;
        }
        if (*valid_state_generated_flag == FALSE)
          ++(*number_invalid_generated_states);
        new_cost_state_2 = current_generated_state->cost;

        /* restore the parameter state */
        current_generated_state->parameter[index_v] = parameter_v;

        /* calculate and store the curvature */
        curvature[index_v_vv] =
          (new_cost_state_2 - TWO * recent_best_cost
           + new_cost_state_1) / (delta_parameter_v * delta_parameter_v
                                  * parameter_v * parameter_v +
                                  (double) EPS_DOUBLE);
      }
    }

    /* calculate off-diagonal curvatures */
    VFOR (index_v) {
      delta_parameter_v = OPTIONS->Delta_X;
      if (delta_parameter_v < SMALL_FLOAT) {
        VFOR (index_vv) {
          /* index_v_vv: row index_v, column index_vv */
          index_v_vv = ROW_COL_INDEX (index_v, index_vv);
          index_vv_v = ROW_COL_INDEX (index_vv, index_v);
          curvature[index_vv_v] = curvature[index_v_vv] = ZERO;
        }
        continue;
      }

      /* save the v_th parameter and delta_x */
      parameter_v = current_generated_state->parameter[index_v];

      VFOR (index_vv) {
        /* index_v_vv: row index_v, column index_vv */
        index_v_vv = ROW_COL_INDEX (index_v, index_vv);
        index_vv_v = ROW_COL_INDEX (index_vv, index_v);

        if (NO_REANNEAL (index_vv) || NO_REANNEAL (index_v)) {
          curvature[index_vv_v] = curvature[index_v_vv] = ZERO;
          continue;
        }
        /* calculate only the upper diagonal */
        if (index_v <= index_vv) {
          continue;
        }
        /* skip parms with too small range or integer parameters */
        if (OPTIONS->Include_Integer_Parameters == TRUE) {
          if (PARAMETER_RANGE_TOO_SMALL (index_v) ||
              PARAMETER_RANGE_TOO_SMALL (index_vv)) {
            curvature[index_vv_v] = curvature[index_v_vv] = ZERO;
            continue;
          }
        } else {
          if (INTEGER_PARAMETER (index_v) ||
              INTEGER_PARAMETER (index_vv) ||
              PARAMETER_RANGE_TOO_SMALL (index_v) ||
              PARAMETER_RANGE_TOO_SMALL (index_vv)) {
            curvature[index_vv_v] = curvature[index_v_vv] = ZERO;
            continue;
          }
        }
        delta_parameter_vv = OPTIONS->Delta_X;
        if (delta_parameter_vv < SMALL_FLOAT) {
          curvature[index_vv_v] = curvature[index_v_vv] = ZERO;
          continue;
        }

        /* save the vv_th parameter and delta_parameter */
        parameter_vv = current_generated_state->parameter[index_vv];

        /* generate first sample point */
        parameter_v_offset = current_generated_state->parameter[index_v] =
          (ONE + delta_parameter_v) * parameter_v;
        parameter_vv_offset = current_generated_state->parameter[index_vv] =
          (ONE + delta_parameter_vv) * parameter_vv;
        if (parameter_v_offset > parameter_maximum[index_v] ||
            parameter_v_offset < parameter_minimum[index_v]) {
          delta_parameter_v = -delta_parameter_v;
          current_generated_state->parameter[index_v] =
            (ONE + delta_parameter_v) * parameter_v;
        }
        if (parameter_vv_offset > parameter_maximum[index_vv] ||
            parameter_vv_offset < parameter_minimum[index_vv]) {
          delta_parameter_vv = -delta_parameter_vv;
          current_generated_state->parameter[index_vv] =
            (ONE + delta_parameter_vv) * parameter_vv;
        }

        *valid_state_generated_flag = TRUE;
        current_generated_state->cost =
          user_cost_function (current_generated_state->parameter,
                              parameter_minimum,
                              parameter_maximum,
                              tangents,
                              curvature,
                              number_parameters,
                              parameter_type,
                              valid_state_generated_flag,
                              exit_status, OPTIONS);
        if ((*valid_state_generated_flag == FALSE)
            || ((current_generated_state->cost) !=
                (current_generated_state->cost))
            || current_generated_state->cost < -MAX_DOUBLE
            || current_generated_state->cost > MAX_DOUBLE) {
          *exit_status = INVALID_COST_FUNCTION_DERIV;
          return;
        }
        if (*valid_state_generated_flag == FALSE)
          ++(*number_invalid_generated_states);
        new_cost_state_1 = current_generated_state->cost;

        /* restore the v_th parameter */
        current_generated_state->parameter[index_v] = parameter_v;

        /* generate second sample point */
        *valid_state_generated_flag = TRUE;
        current_generated_state->cost =
          user_cost_function (current_generated_state->parameter,
                              parameter_minimum,
                              parameter_maximum,
                              tangents,
                              curvature,
                              number_parameters,
                              parameter_type,
                              valid_state_generated_flag,
                              exit_status, OPTIONS);
        if ((*valid_state_generated_flag == FALSE)
            || ((current_generated_state->cost) !=
                (current_generated_state->cost))
            || current_generated_state->cost < -MAX_DOUBLE
            || current_generated_state->cost > MAX_DOUBLE) {
          *exit_status = INVALID_COST_FUNCTION_DERIV;
          return;
        }
        if (*valid_state_generated_flag == FALSE)
          ++(*number_invalid_generated_states);
        new_cost_state_2 = current_generated_state->cost;

        /* restore the vv_th parameter */
        current_generated_state->parameter[index_vv] = parameter_vv;

        /* generate third sample point */
        current_generated_state->parameter[index_v] =
          (ONE + delta_parameter_v) * parameter_v;
        *valid_state_generated_flag = TRUE;
        current_generated_state->cost =
          user_cost_function (current_generated_state->parameter,
                              parameter_minimum,
                              parameter_maximum,
                              tangents,
                              curvature,
                              number_parameters,
                              parameter_type,
                              valid_state_generated_flag,
                              exit_status, OPTIONS);
        if ((*valid_state_generated_flag == FALSE)
            || ((current_generated_state->cost) !=
                (current_generated_state->cost))
            || current_generated_state->cost < -MAX_DOUBLE
            || current_generated_state->cost > MAX_DOUBLE) {
          *exit_status = INVALID_COST_FUNCTION_DERIV;
          return;
        }
        if (*valid_state_generated_flag == FALSE)
          ++(*number_invalid_generated_states);
        new_cost_state_3 = current_generated_state->cost;

        /* restore the v_th parameter */
        current_generated_state->parameter[index_v] = parameter_v;

        /* calculate and store the curvature */
        curvature[index_vv_v] = curvature[index_v_vv] =
          (new_cost_state_1 - new_cost_state_2
           - new_cost_state_3 + recent_best_cost)
          / (delta_parameter_v * delta_parameter_vv
             * parameter_v * parameter_vv + (double) EPS_DOUBLE);
      }
    }
  }

  /* restore Immediate_Exit flag */
  OPTIONS->Immediate_Exit = immediate_flag;

  /* restore the best cost function value */
  current_generated_state->cost = recent_best_cost;
  *number_invalid_generated_states = saved_num_invalid_gen_states;
}

/***********************************************************************
* asa_test_asa_options
*       Tests user's selected options
***********************************************************************/
int

asa_test_asa_options (seed,
                      parameter_initial_final,
                      parameter_minimum,
                      parameter_maximum,
                      tangents,
                      curvature,
                      number_parameters,
                      parameter_type,
                      valid_state_generated_flag,
                      exit_status, ptr_asa_out, OPTIONS)
     LONG_INT *seed;
     double *parameter_initial_final;
     double *parameter_minimum;
     double *parameter_maximum;
     double *tangents;
     double *curvature;
     ALLOC_INT *number_parameters;
     int *parameter_type;
     int *valid_state_generated_flag;
     int *exit_status;
     FILE *ptr_asa_out;
     USER_DEFINES *OPTIONS;
{
  int invalid, index_v;

  invalid = 0;

  if (seed == NULL) {
    strcpy (exit_msg, "*** seed == NULL ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (parameter_initial_final == NULL) {
    strcpy (exit_msg, "*** parameter_initial_final == NULL ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (parameter_minimum == NULL) {
    strcpy (exit_msg, "*** parameter_minimum == NULL ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (parameter_maximum == NULL) {
    strcpy (exit_msg, "*** parameter_maximum == NULL ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (tangents == NULL) {
    strcpy (exit_msg, "*** tangents == NULL ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if ((OPTIONS->Curvature_0 == FALSE) || (OPTIONS->Curvature_0 == -1)) {
    if (curvature == NULL) {
      strcpy (exit_msg, "*** curvature == NULL ***");
      print_string (ptr_asa_out, exit_msg);
      ++invalid;
    }
  }
  if (number_parameters == NULL) {
    strcpy (exit_msg, "*** number_parameters == NULL ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (parameter_type == NULL) {
    strcpy (exit_msg, "*** parameter_type == NULL ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (valid_state_generated_flag == NULL) {
    strcpy (exit_msg, "*** valid_state_generated_flag == NULL ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (exit_status == NULL) {
    strcpy (exit_msg, "*** exit_status == NULL ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS == NULL) {
    strcpy (exit_msg, "*** OPTIONS == NULL ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }

  VFOR (index_v) if (parameter_minimum[index_v] > parameter_maximum[index_v]) {
    strcpy (exit_msg, "*** parameter_minimum[] > parameter_maximum[] ***");
    print_string_index (ptr_asa_out, exit_msg, index_v);
    ++invalid;
  }
  VFOR (index_v)
    if (parameter_initial_final[index_v] < parameter_minimum[index_v]) {
    if (PARAMETER_RANGE_TOO_SMALL (index_v))
      continue;
    strcpy (exit_msg, "*** parameter_initial[] < parameter_minimum[] ***");
    print_string_index (ptr_asa_out, exit_msg, index_v);
    ++invalid;
  }
  VFOR (index_v)
    if (parameter_initial_final[index_v] > parameter_maximum[index_v]) {
    if (PARAMETER_RANGE_TOO_SMALL (index_v))
      continue;
    strcpy (exit_msg, "*** parameter_initial[] > parameter_maximum[] ***");
    print_string_index (ptr_asa_out, exit_msg, index_v);
    ++invalid;
  }
  if (*number_parameters < 1) {
    strcpy (exit_msg, "*** *number_parameters < 1 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  VFOR (index_v)
    if (parameter_type[index_v] != -2 && parameter_type[index_v] != 2
        && parameter_type[index_v] != -1 && parameter_type[index_v] != 1) {
    strcpy (exit_msg,
            "*** parameter_type[] != -2 && parameter_type[] != 2 && parameter_type[] != -1 && parameter_type[] != 1 ***");
    print_string_index (ptr_asa_out, exit_msg, index_v);
    ++invalid;
  }

  if (OPTIONS_FILE != FALSE && OPTIONS_FILE != TRUE) {
    strcpy (exit_msg,
            "*** OPTIONS_FILE != FALSE && OPTIONS_FILE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS_FILE_DATA != FALSE && OPTIONS_FILE_DATA != TRUE) {
    strcpy (exit_msg,
            "*** OPTIONS_FILE_DATA != FALSE && OPTIONS_FILE_DATA != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (RECUR_OPTIONS_FILE != FALSE && RECUR_OPTIONS_FILE != TRUE) {
    strcpy (exit_msg,
            "*** RECUR_OPTIONS_FILE != FALSE && RECUR_OPTIONS_FILE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (RECUR_OPTIONS_FILE_DATA != FALSE && RECUR_OPTIONS_FILE_DATA != TRUE) {
    strcpy (exit_msg,
            "*** RECUR_OPTIONS_FILE_DATA != FALSE && RECUR_OPTIONS_FILE_DATA != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (COST_FILE != FALSE && COST_FILE != TRUE) {
    strcpy (exit_msg, "*** COST_FILE != FALSE && COST_FILE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_LIB != FALSE && ASA_LIB != TRUE) {
    strcpy (exit_msg, "*** ASA_LIB != FALSE && ASA_LIB != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (MY_TEMPLATE != FALSE && MY_TEMPLATE != TRUE) {
    strcpy (exit_msg, "*** MY_TEMPLATE != FALSE && MY_TEMPLATE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_TEMPLATE_LIB != FALSE && ASA_TEMPLATE_LIB != TRUE) {
    strcpy (exit_msg,
            "*** ASA_TEMPLATE_LIB != FALSE && ASA_TEMPLATE_LIB != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (HAVE_ANSI != FALSE && HAVE_ANSI != TRUE) {
    strcpy (exit_msg, "*** HAVE_ANSI != FALSE && HAVE_ANSI != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (IO_PROTOTYPES != FALSE && IO_PROTOTYPES != TRUE) {
    strcpy (exit_msg,
            "*** IO_PROTOTYPES != FALSE && IO_PROTOTYPES != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (TIME_CALC != FALSE && TIME_CALC != TRUE) {
    strcpy (exit_msg, "*** TIME_CALC != FALSE && TIME_CALC != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (TIME_STD != FALSE && TIME_STD != TRUE) {
    strcpy (exit_msg, "*** TIME_STD != FALSE && TIME_STD != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (TIME_GETRUSAGE != FALSE && TIME_GETRUSAGE != TRUE) {
    strcpy (exit_msg,
            "*** TIME_GETRUSAGE != FALSE && TIME_GETRUSAGE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (INT_LONG != FALSE && INT_LONG != TRUE) {
    strcpy (exit_msg, "*** INT_LONG != FALSE && INT_LONG != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (INT_ALLOC != FALSE && INT_ALLOC != TRUE) {
    strcpy (exit_msg, "*** INT_ALLOC != FALSE && INT_ALLOC != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (SMALL_FLOAT < ZERO) {
    strcpy (exit_msg, "*** SMALL_FLOAT < ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (MIN_DOUBLE < ZERO) {
    strcpy (exit_msg, "*** MIN_DOUBLE < ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (MAX_DOUBLE < ZERO) {
    strcpy (exit_msg, "*** MAX_DOUBLE < ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (EPS_DOUBLE < ZERO) {
    strcpy (exit_msg, "*** EPS_DOUBLE < ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (CHECK_EXPONENT != FALSE && CHECK_EXPONENT != TRUE) {
    strcpy (exit_msg,
            "*** CHECK_EXPONENT != FALSE && CHECK_EXPONENT != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (NO_PARAM_TEMP_TEST != FALSE && NO_PARAM_TEMP_TEST != TRUE) {
    strcpy (exit_msg,
            "*** NO_PARAM_TEMP_TEST != FALSE && NO_PARAM_TEMP_TEST != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (NO_COST_TEMP_TEST != FALSE && NO_COST_TEMP_TEST != TRUE) {
    strcpy (exit_msg,
            "*** NO_COST_TEMP_TEST != FALSE && NO_COST_TEMP_TEST != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (SELF_OPTIMIZE != FALSE && SELF_OPTIMIZE != TRUE) {
    strcpy (exit_msg,
            "*** SELF_OPTIMIZE != FALSE && SELF_OPTIMIZE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_TEST != FALSE && ASA_TEST != TRUE) {
    strcpy (exit_msg, "*** ASA_TEST != FALSE && ASA_TEST != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_TEST_POINT != FALSE && ASA_TEST_POINT != TRUE) {
    strcpy (exit_msg,
            "*** ASA_TEST_POINT != FALSE && ASA_TEST_POINT != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_EXIT_ANYTIME != FALSE && ASA_EXIT_ANYTIME != TRUE) {
    strcpy (exit_msg,
            "*** ASA_EXIT_ANYTIME != FALSE && ASA_EXIT_ANYTIME != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_TEMPLATE != FALSE) {
    strcpy (exit_msg, "*** ASA_TEMPLATE != FALSE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_TEMPLATE_ASA_OUT_PID != FALSE && ASA_TEMPLATE_ASA_OUT_PID != TRUE) {
    strcpy (exit_msg,
            "*** ASA_TEMPLATE_ASA_OUT_PID != FALSE && ASA_TEMPLATE_ASA_OUT_PID != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_TEMPLATE_MULTIPLE != FALSE && ASA_TEMPLATE_MULTIPLE != TRUE) {
    strcpy (exit_msg,
            "*** ASA_TEMPLATE_MULTIPLE != FALSE && ASA_TEMPLATE_MULTIPLE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_TEMPLATE_SELFOPT != FALSE && ASA_TEMPLATE_SELFOPT != TRUE) {
    strcpy (exit_msg,
            "*** ASA_TEMPLATE_SELFOPT != FALSE && ASA_TEMPLATE_SELFOPT != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_TEMPLATE_SAMPLE != FALSE && ASA_TEMPLATE_SAMPLE != TRUE) {
    strcpy (exit_msg,
            "*** ASA_TEMPLATE_SAMPLE != FALSE && ASA_TEMPLATE_SAMPLE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_TEMPLATE_QUEUE != FALSE && ASA_TEMPLATE_QUEUE != TRUE) {
    strcpy (exit_msg,
            "*** ASA_TEMPLATE_QUEUE != FALSE && ASA_TEMPLATE_QUEUE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_TEMPLATE_PARALLEL != FALSE && ASA_TEMPLATE_PARALLEL != TRUE) {
    strcpy (exit_msg,
            "*** ASA_TEMPLATE_PARALLEL != FALSE && ASA_TEMPLATE_PARALLEL != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_TEMPLATE_SAVE != FALSE && ASA_TEMPLATE_SAVE != TRUE) {
    strcpy (exit_msg,
            "*** ASA_TEMPLATE_SAVE != FALSE && ASA_TEMPLATE_SAVE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (USER_INITIAL_COST_TEMP != FALSE && USER_INITIAL_COST_TEMP != TRUE) {
    strcpy (exit_msg,
            "*** USER_INITIAL_COST_TEMP != FALSE && USER_INITIAL_COST_TEMP != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (RATIO_TEMPERATURE_SCALES != FALSE && RATIO_TEMPERATURE_SCALES != TRUE) {
    strcpy (exit_msg,
            "*** RATIO_TEMPERATURE_SCALES != FALSE && RATIO_TEMPERATURE_SCALES != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (USER_INITIAL_PARAMETERS_TEMPS != FALSE
      && USER_INITIAL_PARAMETERS_TEMPS != TRUE) {
    strcpy (exit_msg,
            "*** USER_INITIAL_PARAMETERS_TEMPS != FALSE && USER_INITIAL_PARAMETERS_TEMPS != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (DELTA_PARAMETERS != FALSE && DELTA_PARAMETERS != TRUE) {
    strcpy (exit_msg,
            "*** DELTA_PARAMETERS != FALSE && DELTA_PARAMETERS != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (QUENCH_PARAMETERS != FALSE && QUENCH_PARAMETERS != TRUE) {
    strcpy (exit_msg,
            "*** QUENCH_PARAMETERS != FALSE && QUENCH_PARAMETERS != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (QUENCH_COST != FALSE && QUENCH_COST != TRUE) {
    strcpy (exit_msg, "*** QUENCH_COST != FALSE && QUENCH_COST != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (QUENCH_PARAMETERS_SCALE != FALSE && QUENCH_PARAMETERS_SCALE != TRUE) {
    strcpy (exit_msg,
            "*** QUENCH_PARAMETERS_SCALE != FALSE && QUENCH_PARAMETERS_SCALE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (QUENCH_COST_SCALE != FALSE && QUENCH_COST_SCALE != TRUE) {
    strcpy (exit_msg,
            "*** QUENCH_COST_SCALE != FALSE && QUENCH_COST_SCALE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONAL_DATA_DBL != FALSE && OPTIONAL_DATA_DBL != TRUE) {
    strcpy (exit_msg,
            "*** OPTIONAL_DATA_DBL != FALSE && OPTIONAL_DATA_DBL != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONAL_DATA_INT != FALSE && OPTIONAL_DATA_INT != TRUE) {
    strcpy (exit_msg,
            "*** OPTIONAL_DATA_INT != FALSE && OPTIONAL_DATA_INT != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONAL_DATA_PTR != FALSE && OPTIONAL_DATA_PTR != TRUE) {
    strcpy (exit_msg,
            "*** OPTIONAL_DATA_PTR != FALSE && OPTIONAL_DATA_PTR != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (USER_COST_SCHEDULE != FALSE && USER_COST_SCHEDULE != TRUE) {
    strcpy (exit_msg,
            "*** USER_COST_SCHEDULE != FALSE && USER_COST_SCHEDULE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (USER_ACCEPT_ASYMP_EXP != FALSE && USER_ACCEPT_ASYMP_EXP != TRUE) {
    strcpy (exit_msg,
            "*** USER_ACCEPT_ASYMP_EXP != FALSE && USER_ACCEPT_ASYMP_EXP != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (USER_ACCEPT_THRESHOLD != FALSE && USER_ACCEPT_THRESHOLD != TRUE) {
    strcpy (exit_msg,
            "*** USER_ACCEPT_THRESHOLD != FALSE && USER_ACCEPT_THRESHOLD != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (USER_ACCEPTANCE_TEST != FALSE && USER_ACCEPTANCE_TEST != TRUE) {
    strcpy (exit_msg,
            "*** USER_ACCEPTANCE_TEST != FALSE && USER_ACCEPTANCE_TEST != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (USER_GENERATING_FUNCTION != FALSE && USER_GENERATING_FUNCTION != TRUE) {
    strcpy (exit_msg,
            "*** USER_GENERATING_FUNCTION != FALSE && USER_GENERATING_FUNCTION != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (USER_REANNEAL_COST != FALSE && USER_REANNEAL_COST != TRUE) {
    strcpy (exit_msg,
            "*** USER_REANNEAL_COST != FALSE && USER_REANNEAL_COST != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (USER_REANNEAL_PARAMETERS != FALSE && USER_REANNEAL_PARAMETERS != TRUE) {
    strcpy (exit_msg,
            "*** USER_REANNEAL_PARAMETERS != FALSE && USER_REANNEAL_PARAMETERS != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (MAXIMUM_REANNEAL_INDEX < 1) {
    strcpy (exit_msg, "*** MAXIMUM_REANNEAL_INDEX < 1 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (REANNEAL_SCALE < ZERO) {
    strcpy (exit_msg, "*** REANNEAL_SCALE < ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_SAMPLE != FALSE && ASA_SAMPLE != TRUE) {
    strcpy (exit_msg, "*** ASA_SAMPLE != FALSE && ASA_SAMPLE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ADAPTIVE_OPTIONS != FALSE && ADAPTIVE_OPTIONS != TRUE) {
    strcpy (exit_msg,
            "*** ADAPTIVE_OPTIONS != FALSE && ADAPTIVE_OPTIONS != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_QUEUE != FALSE && ASA_QUEUE != TRUE) {
    strcpy (exit_msg, "*** ASA_QUEUE != FALSE && ASA_QUEUE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_RESOLUTION != FALSE && ASA_RESOLUTION != TRUE) {
    strcpy (exit_msg,
            "*** ASA_RESOLUTION != FALSE && ASA_RESOLUTION != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_FUZZY != FALSE && ASA_FUZZY != TRUE) {
    strcpy (exit_msg, "*** ASA_FUZZY != FALSE && ASA_FUZZY != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (FITLOC != FALSE && FITLOC != TRUE) {
    strcpy (exit_msg, "*** FITLOC != FALSE && FITLOC != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (FITLOC_ROUND != FALSE && FITLOC_ROUND != TRUE) {
    strcpy (exit_msg,
            "*** FITLOC_ROUND != FALSE && FITLOC_ROUND != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (FITLOC_PRINT != FALSE && FITLOC_PRINT != TRUE) {
    strcpy (exit_msg,
            "*** FITLOC_PRINT != FALSE && FITLOC_PRINT != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (MULTI_MIN != FALSE && MULTI_MIN != TRUE) {
    strcpy (exit_msg, "*** MULTI_MIN != FALSE && MULTI_MIN != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_PARALLEL != FALSE && ASA_PARALLEL != TRUE) {
    strcpy (exit_msg,
            "*** ASA_PARALLEL != FALSE && ASA_PARALLEL != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_SAVE != FALSE && ASA_SAVE != TRUE) {
    strcpy (exit_msg, "*** ASA_SAVE != FALSE && ASA_SAVE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_SAVE_OPT != FALSE && ASA_SAVE_OPT != TRUE) {
    strcpy (exit_msg,
            "*** ASA_SAVE_OPT != FALSE && ASA_SAVE_OPT != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_SAVE_BACKUP != FALSE && ASA_SAVE_BACKUP != TRUE) {
    strcpy (exit_msg,
            "*** ASA_SAVE_BACKUP != FALSE && ASA_SAVE_BACKUP != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_PIPE != FALSE && ASA_PIPE != TRUE) {
    strcpy (exit_msg, "*** ASA_PIPE != FALSE && ASA_PIPE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_PIPE_FILE != FALSE && ASA_PIPE_FILE != TRUE) {
    strcpy (exit_msg,
            "*** ASA_PIPE_FILE != FALSE && ASA_PIPE_FILE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (SYSTEM_CALL != FALSE && SYSTEM_CALL != TRUE) {
    strcpy (exit_msg, "*** SYSTEM_CALL != FALSE && SYSTEM_CALL != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (FDLIBM_POW != FALSE && FDLIBM_POW != TRUE) {
    strcpy (exit_msg, "*** FDLIBM_POW != FALSE && FDLIBM_POW != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (FDLIBM_LOG != FALSE && FDLIBM_LOG != TRUE) {
    strcpy (exit_msg, "*** FDLIBM_LOG != FALSE && FDLIBM_LOG != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (FDLIBM_EXP != FALSE && FDLIBM_EXP != TRUE) {
    strcpy (exit_msg, "*** FDLIBM_EXP != FALSE && FDLIBM_EXP != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_PRINT != FALSE && ASA_PRINT != TRUE) {
    strcpy (exit_msg, "*** ASA_PRINT != FALSE && ASA_PRINT != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (USER_ASA_OUT != FALSE && USER_ASA_OUT != TRUE) {
    strcpy (exit_msg,
            "*** USER_ASA_OUT != FALSE && USER_ASA_OUT != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_PRINT_INTERMED != FALSE && ASA_PRINT_INTERMED != TRUE) {
    strcpy (exit_msg,
            "*** ASA_PRINT_INTERMED != FALSE && ASA_PRINT_INTERMED != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (ASA_PRINT_MORE != FALSE && ASA_PRINT_MORE != TRUE) {
    strcpy (exit_msg,
            "*** ASA_PRINT_MORE != FALSE && ASA_PRINT_MORE != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (G_FIELD < 0) {
    strcpy (exit_msg, "*** G_FIELD < 0 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (G_PRECISION < 0) {
    strcpy (exit_msg, "*** G_PRECISION < 0 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }

  if (OPTIONS->Limit_Acceptances < 0) {
    strcpy (exit_msg, "*** Limit_Acceptances < 0 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Limit_Generated < 0) {
    strcpy (exit_msg, "*** Limit_Generated < 0 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Limit_Invalid_Generated_States < 0) {
    strcpy (exit_msg, "*** Limit_Invalid_Generated_States < 0 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Accepted_To_Generated_Ratio <= ZERO) {
    strcpy (exit_msg, "*** Accepted_To_Generated_Ratio <= ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Cost_Precision <= ZERO) {
    strcpy (exit_msg, "*** Cost_Precision <= ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Maximum_Cost_Repeat < 0) {
    strcpy (exit_msg, "*** Maximum_Cost_Repeat < 0 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Number_Cost_Samples == 0 || OPTIONS->Number_Cost_Samples == -1) {
    strcpy (exit_msg,
            "*** Number_Cost_Samples == 0 || Number_Cost_Samples == -1 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Temperature_Ratio_Scale <= ZERO) {
    strcpy (exit_msg, "*** Temperature_Ratio_Scale <= ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Cost_Parameter_Scale_Ratio <= ZERO) {
    strcpy (exit_msg, "*** Cost_Parameter_Scale_Ratio <= ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Temperature_Anneal_Scale <= ZERO) {
    strcpy (exit_msg, "*** Temperature_Anneal_Scale <= ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Include_Integer_Parameters != FALSE
      && OPTIONS->Include_Integer_Parameters != TRUE) {
    strcpy (exit_msg, "");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->User_Initial_Parameters != FALSE
      && OPTIONS->User_Initial_Parameters != TRUE) {
    strcpy (exit_msg,
            "*** User_Initial_Parameters != FALSE && User_Initial_Parameters != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Sequential_Parameters >= *number_parameters) {
    strcpy (exit_msg, "*** Sequential_Parameters >= *number_parameters ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Initial_Parameter_Temperature <= ZERO) {
    strcpy (exit_msg, "*** Initial_Parameter_Temperature <= ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Acceptance_Frequency_Modulus < 0) {
    strcpy (exit_msg, "*** Acceptance_Frequency_Modulus < 0 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Generated_Frequency_Modulus < 0) {
    strcpy (exit_msg, "*** Generated_Frequency_Modulus < 0 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Reanneal_Cost == -1) {
    strcpy (exit_msg, "*** Reanneal_Cost == -1 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Reanneal_Parameters != FALSE
      && OPTIONS->Reanneal_Parameters != TRUE) {
    strcpy (exit_msg,
            "*** Reanneal_Parameters != FALSE && Reanneal_Parameters != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Delta_X < ZERO) {
    strcpy (exit_msg, "*** Delta_X < ZERO ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->User_Tangents != FALSE && OPTIONS->User_Tangents != TRUE) {
    strcpy (exit_msg,
            "*** User_Tangents != FALSE && User_Tangents != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Curvature_0 != -1 && OPTIONS->Curvature_0 != FALSE
      && OPTIONS->Curvature_0 != TRUE) {
    strcpy (exit_msg,
            "*** Curvature_0 -1 && Curvature_0 != FALSE && Curvature_0 != TRUE ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Asa_Data_Dim_Ptr < 1) {
    strcpy (exit_msg, "*** Asa_Data_Dim_Ptr < 1 ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }
  if (OPTIONS->Asa_Data_Ptr == NULL) {
    strcpy (exit_msg, "*** Asa_Data_Ptr == NULL ***");
    print_string (ptr_asa_out, exit_msg);
    ++invalid;
  }

  return (invalid);
}

/***********************************************************************
* cost_function_test
*       Tests user's returned cost function values and parameters
***********************************************************************/
int

cost_function_test (cost,
                    parameter,
                    parameter_minimum, parameter_maximum,
                    number_parameters, xnumber_parameters)
     double cost;
     double *parameter;
     double *parameter_minimum;
     double *parameter_maximum;
     ALLOC_INT *number_parameters;
     double *xnumber_parameters;
{
  ALLOC_INT index_v;
  int test_flag;

  test_flag = 1;

  if (((cost) != (cost)) || (cost < -MAX_DOUBLE || cost > MAX_DOUBLE))
    test_flag = 0;

  *xnumber_parameters = (double) *number_parameters;
  VFOR (index_v) {
    if (PARAMETER_RANGE_TOO_SMALL (index_v)) {
      *xnumber_parameters -= 1.0;
      continue;
    }
    if (parameter[index_v] < parameter_minimum[index_v] ||
        parameter[index_v] > parameter_maximum[index_v]) {
      test_flag = 0;
    }
  }

  return (test_flag);
}

/***********************************************************************
* print_string
*	This prints the designated string
***********************************************************************/
void
print_string (ptr_asa_out, string)
     FILE *ptr_asa_out;
     char *string;
{
}

/***********************************************************************
* print_string_index
*	This prints the designated string and index
***********************************************************************/
void
print_string_index (ptr_asa_out, string, index)
     FILE *ptr_asa_out;
     char *string;
     ALLOC_INT index;
{

  ;
}




void
Exit_ASA (statement)
     char *statement;
{
  ;
}
