/**
 * @cond doxygenLibsbmlInternal
 *
 * @file    FunctionDefinitionRecursion.h
 * @brief   Checks for recursion in functionDefinitions
 * @author  Sarah Keating
 * 
 * <!--------------------------------------------------------------------------
 * This file is part of libSBML.  Please visit http://sbml.org for more
 * information about SBML, and the latest version of libSBML.
 *
 * Copyright (C) 2013-2017 jointly by the following organizations:
 *     1. California Institute of Technology, Pasadena, CA, USA
 *     2. EMBL European Bioinformatics Institute (EMBL-EBI), Hinxton, UK
 *     3. University of Heidelberg, Heidelberg, Germany
 *
 * Copyright (C) 2009-2013 jointly by the following organizations: 
 *     1. California Institute of Technology, Pasadena, CA, USA
 *     2. EMBL European Bioinformatics Institute (EMBL-EBI), Hinxton, UK
 *  
 * Copyright (C) 2006-2008 by the California Institute of Technology,
 *     Pasadena, CA, USA 
 *  
 * Copyright (C) 2002-2005 jointly by the following organizations: 
 *     1. California Institute of Technology, Pasadena, CA, USA
 *     2. Japan Science and Technology Agency, Japan
 * 
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation.  A copy of the license agreement is provided
 * in the file named "LICENSE.txt" included with this software distribution
 * and also available online as http://sbml.org/software/libsbml/license.html
 * ---------------------------------------------------------------------- -->*/

#ifndef FunctionDefinitionRecursion_h
#define FunctionDefinitionRecursion_h


#ifdef __cplusplus

#include <string>

#include <sbml/validator/VConstraint.h>

#include <sbml/util/IdList.h>

LIBSBML_CPP_NAMESPACE_BEGIN

typedef std::multimap<const std::string, std::string> IdMap;
typedef IdMap::iterator                               IdIter;
typedef std::pair<IdIter, IdIter>                     IdRange;

class FunctionDefinitionRecursion: public TConstraint<Model>
{
public:

  /**
   * Creates a new Constraint with the given constraint id.
   */
  FunctionDefinitionRecursion (unsigned int id, Validator& v);

  /**
   * Destroys this Constraint.
   */
  virtual ~FunctionDefinitionRecursion ();


protected:

  /**
   * Checks for recursion in functions
   */
  virtual void check_ (const Model& m, const Model& object);

  
  /* create pairs of ids that depend on each other */
  void addDependencies(const Model &, const FunctionDefinition &);

  
  void determineAllDependencies();


  /* helper function to check if a pair already exists */
  bool alreadyExistsInMap(IdMap map, 
                          std::pair<const std::string, std::string> dependency);

  
  /* check for explicit use of original variable */
  void checkForSelfAssignment(const Model &);


  /* find cycles in the map of dependencies */
  void determineCycles(const Model& m);

  /**
   * Logs a message about recursion in the given
   * FunctionDefinition.
   */

  void logSelfRecursion (const FunctionDefinition& fd, const std::string& varname);

  void logCycle (const FunctionDefinition* object, const FunctionDefinition* conflict);


  IdMap mIdMap;

};

LIBSBML_CPP_NAMESPACE_END

#endif  /* __cplusplus */
#endif  /* FunctionDefinitionRecursion_h */
/** @endcond */
