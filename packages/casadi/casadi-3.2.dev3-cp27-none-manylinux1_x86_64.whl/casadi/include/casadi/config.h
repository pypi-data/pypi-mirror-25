/*
 *    This file is part of CasADi.
 *
 *    CasADi -- A symbolic framework for dynamic optimization.
 *    Copyright (C) 2010-2014 Joel Andersson, Joris Gillis, Moritz Diehl,
 *                            K.U. Leuven. All rights reserved.
 *    Copyright (C) 2011-2014 Greg Horn
 *
 *    CasADi is free software; you can redistribute it and/or
 *    modify it under the terms of the GNU Lesser General Public
 *    License as published by the Free Software Foundation; either
 *    version 3 of the License, or (at your option) any later version.
 *
 *    CasADi is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *    Lesser General Public License for more details.
 *
 *    You should have received a copy of the GNU Lesser General Public
 *    License along with CasADi; if not, write to the Free Software
 *    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */
#ifndef BUILD_CASADI_CONFIG_H_
#define BUILD_CASADI_CONFIG_H_

#define CASADI_MAJOR_VERSION 3
#define CASADI_MINOR_VERSION 2
#define CASADI_PATCH_VERSION 2
#define CASADI_IS_RELEASE 1
#define CASADI_VERSION_STRING "3.2.2"
#define CASADI_GIT_REVISION "2aa438fac2c7fad23d073b152f4245cef5cdde28"  // NOLINT(whitespace/line_length)
#define CASADI_GIT_DESCRIBE ""  // NOLINT(whitespace/line_length)
#define CASADI_FEATURE_LIST ""  // NOLINT(whitespace/line_length)
#define CASADI_BUILD_TYPE "Release"  // NOLINT(whitespace/line_length)
#define CASADI_COMPILER_ID "GNU"  // NOLINT(whitespace/line_length)
#define CASADI_COMPILER "/opt/rh/devtoolset-2/root/usr/bin/g++"  // NOLINT(whitespace/line_length)
#define CASADI_COMPILER_FLAGS " -std=c++11 -fPIC -fvisibility=hidden -fvisibility-inlines-hidden   "  // NOLINT(whitespace/line_length)
#define CASADI_MODULES "casadi;casadi_sundials_common;casadi_integrator_cvodes;casadi_integrator_idas;casadi_rootfinder_kinsol;casadi_nlpsol_ipopt;casadi_linsol_csparse;casadi_linsol_csparsecholesky;casadi_linsol_ma27;casadi_xmlfile_tinyxml;casadi_conic_hpmpc;casadi_conic_nlpsol;casadi_importer_shell;casadi_integrator_rk;casadi_integrator_collocation;casadi_interpolant_linear;casadi_interpolant_bspline;casadi_linsol_symbolicqr;casadi_linsol_lsqr;casadi_nlpsol_sqpmethod;casadi_nlpsol_scpgen;casadi_rootfinder_newton;casadi_rootfinder_nlpsol"  // NOLINT(whitespace/line_length)
#define CASADI_PLUGINS "Integrator::cvodes;Integrator::idas;Rootfinder::kinsol;Nlpsol::ipopt;Linsol::csparse;Linsol::csparsecholesky;Linsol::ma27;XmlFile::tinyxml;Conic::hpmpc;Conic::nlpsol;Importer::shell;Integrator::rk;Integrator::collocation;Interpolant::linear;Interpolant::bspline;Linsol::symbolicqr;Linsol::lsqr;Nlpsol::sqpmethod;Nlpsol::scpgen;Rootfinder::newton;Rootfinder::nlpsol"  // NOLINT(whitespace/line_length)
#define CASADI_INSTALL_PREFIX "/home/travis/build/casadi/binaries/casadi/python_install"  // NOLINT(whitespace/line_length)

#endif  // BUILD_CASADI_CONFIG_H_
