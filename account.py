# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2012 OpenERP - Team de Localización Argentina.
# https://launchpad.net/~openerp-l10n-ar-localization
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from datetime import date

class account_invoice(osv.osv):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    def _check_certificate_nbr(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
	if obj.certificate_nbr and obj.type == 'in_invoice':
		data = obj.certificate_nbr.split('-')
		if len(data) < 3:
			return False
		try:
			cert_nbr = int(data[2])
		except:
			return False
		# Largo de cada uno de los campos
		if len(data[0]) <> 4 or len(data[1]) <> 4 or len(data[2]) <> 6:
			return False
		# Cambio de año
		if cert_nbr in [0,1]:
			current_year = date.today().year 
			try:
				old_year = int(data[1])
			except:
				return False

			if current_year == old_year:
				return True

		# Secuencialidad

		new_cert = str(cert_nbr - 1)
		z_new_cert = new_cert.zfill(6)

		new_cert = data[0] + '-' + data[1] + '-' + z_new_cert
		invoice_id = self.search(cr,uid,[('certificate_nbr','=',new_cert)])

		if not invoice_id:
			return False

	
        return True

    _columns = {
        'certificate_nbr': fields.char('Certificate Nbr',size=32),
    }

    _default = {
	'certificate_nbr': '',
	}

    _constraints = [
        (_check_certificate_nbr, 'Nro de certificado no correlativo', ['certificate_nbr']),
    ]

account_invoice()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
