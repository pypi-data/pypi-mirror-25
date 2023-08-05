/* See https://www.python-ldap.org/ for details.
 * $Id: options.h,v 1.5 2017/08/15 16:21:59 stroeder Exp $ */

int	LDAP_optionval_by_name(const char *name);
int	LDAP_set_option(LDAPObject *self, int option, PyObject *value);
PyObject *LDAP_get_option(LDAPObject *self, int option);

void set_timeval_from_double( struct timeval *tv, double d );
