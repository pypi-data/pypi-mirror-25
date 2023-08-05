/**
 * @file libcombine-version.cpp
 * @brief Implementation of the libcombine-version class.
 * @author DEVISER
 *
 * <!--------------------------------------------------------------------------
 * This file is part of libSBML. Please visit http://sbml.org for more
 * information about SBML, and the latest version of libSBML.
 *
 * Copyright (C) 2013-2016 jointly by the following organizations:
 * 1. California Institute of Technology, Pasadena, CA, USA
 * 2. EMBL European Bioinformatics Institute (EMBL-EBI), Hinxton, UK
 * 3. University of Heidelberg, Heidelberg, Germany
 *
 * Copyright (C) 2009-2013 jointly by the following organizations:
 * 1. California Institute of Technology, Pasadena, CA, USA
 * 2. EMBL European Bioinformatics Institute (EMBL-EBI), Hinxton, UK
 *
 * Copyright (C) 2006-2008 by the California Institute of Technology,
 * Pasadena, CA, USA
 *
 * Copyright (C) 2002-2005 jointly by the following organizations:
 * 1. California Institute of Technology, Pasadena, CA, USA
 * 2. Japan Science and Technology Agency, Japan
 *
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by the
 * Free Software Foundation. A copy of the license agreement is provided in the
 * file named "LICENSE.txt" included with this software distribution and also
 * available online as http://sbml.org/software/libsbml/license.html
 * ------------------------------------------------------------------------ -->
 */



#include "omex/common/libcombine-version.h"
#include <string.h>


LIBCOMBINE_CPP_NAMESPACE_BEGIN

LIBCOMBINE_EXTERN
int 
getLibCombineVersion() 
{ 
  return LIBCOMBINE_VERSION; 
}


LIBCOMBINE_EXTERN
const char* 
getLibCombineDottedVersion() 
{ 
  return LIBCOMBINE_DOTTED_VERSION;
}


LIBCOMBINE_EXTERN
const char* 
getLibCombineVersionString() 
{ 
  return LIBCOMBINE_VERSION_STRING;
}

LIBCOMBINE_CPP_NAMESPACE_END


