import argparse
import os
import sys


parser = argparse.ArgumentParser(description='Convert Packmol file to LAMMPS Data File')
parser.add_argument('-f','--file', help='Provide filename with ', default='',required=True)
parser.add_argument('-m','--methane',help='#molecule1',required = True)
parser.add_argument('-w','--water',help='#water',default=0,required=True)
args = vars(parser.parse_args())

# usage python2 packman_point_molecules.py -f filename.xyz -c 47 -h 47 > out.txt

# atoms types
atom_type = {'O': 1, 'H1': 2, 'C': 3, 'H2': 4}

# Number of water and methane molecules
molecules_no = []
molecules_no.append(int(args['water']))
molecules_no.append(int(args['methane']))

# partial charges 					  methane   water
partial_charges = {'C': 0,  'H2': -0.053, 'H1':0.520, 'O': -1.040}
angles = {'H2O':1,'CH4':6}

# read file
print " " 
print 3*molecules_no[0] + 1*molecules_no[1],"atoms"
print 2*molecules_no[0], "bonds"
print 1*molecules_no[0],"angles"
print " "

with open(args['file']) as f:
	next(f)
	next(f)
	####### Atom Section #######
	print "Atoms\n"
	atom_id = 1
	molecule_id = 1
	for line in f:
		line = line.split()
		atom = line[0]
		print atom_id,
		# print 1 if atom_id <= 3*molecules_no[0] else 2, # molecule ID
		print molecule_id,
		# check if atom is H, then find which H it is
		if atom == 'H':
			atom = 'H1' if atom_id <= 3*molecules_no[0] else 'H2'
		print atom_type[atom],
		print partial_charges[atom],

		# co-ordinates
		for i in range(1, 4):
			print line[i],
		# initial velocities
		for i in range(3):
			print 0,

		# increment molecule ID
		if molecule_id <= molecules_no[0]:
			if atom_id%3 == 0:
				molecule_id += 1
		else:
			molecule_id += 1
		print 
		atom_id += 1
	print '\n'

	####### Bond section #######
	"""
	Format: Bond ID, Bond type, Atom_1 ID, Atom_2 ID
	ID = bond number (1-Nbonds)
	type = bond type (1-Nbondtype)
	atom1,atom2 = IDs of 1st,2nd atoms in bond  
	NOTE: Atom_1 ID < Atom_2 ID
	Example:
	12 3 17 29
	"""
	bond_id = 1
	bond_type = {'O-H': 1, 'C-H': 2}
	total_bonds = molecules_no[0]*2 + molecules_no[1]*4
	atom_1, atom_2 = 2, 1	 # initial ids for first O-H bond
	print "Bonds\n"
	for _ in range(total_bonds):
		print bond_id,
		print bond_type['O-H'] if bond_id <= molecules_no[0]*2 else bond_type['C-H'],
		print atom_2,
		print atom_1,
		print
		# increment atom ids
		if bond_id < molecules_no[0]*2:
			if(bond_id%2 == 0):
				atom_2 = atom_1 + 1
				atom_1 = atom_2 + 1

			else:
				atom_1 += 1
		else:
			break

		bond_id += 1

	print '\n' 
	####### Angles Section #######
	"""
	Format: Angle ID, Angle type, Atom_1 ID, Atom_2 ID, Atom_3 ID
	ID = number of angle (1-Nangles)
	type = angle type (1-Nangletype)
	atom1,atom2,atom3 = IDs of 1st,2nd,3rd atoms in angle
	The 3 atoms are ordered linearly within the angle. Thus the central atom (around which the angle is computed) is the atom2 in the list. 
	E.g. H,O,H for a water molecule. The Angles section must appear after the Atoms section. All values in this section must be integers (1, not 1.0).
	
	Example:
	2 2 17 29 430
	"""
	print "Angles\n"
	angle_id = 1
	angle_type = {'H-O-H': 1, 'H-C-H': 2}
	total_angles = molecules_no[0]*angles['H2O'] + molecules_no[1]*angles['CH4']
	atom_1, atom_2, atom_3 = 2, 1, 3 # intial ids for first H-O-H angle
	for _ in range(total_angles):
		print angle_id,
		print angle_type['H-O-H'] if angle_id <= molecules_no[0]*1 else angle_type['H-C-H'],
		print atom_1,
		print atom_2,
		print atom_3,
		print
		# increment atom ids
		if angle_id < molecules_no[0]*1:
			atom_1 += 3
			atom_2 += 3
			atom_3 += 3
		else:
			break
		angle_id += 1
