######################################################################################
#
# Python script create_poly_rings.py written by Joseph Patton (@JosephPattonWx
# on Twitter). Script last edited on 3 August, 2021.
#
######################################################################################
#
# This is a python script intended to create holes (rings) within the SPC
# severe weather outlook polygons which are archived in the IEM database here:
# www.mesonet.agron.iastate.edu/request/gis/spc_outlooks.phtml
#
#
# The SPC severe weather outlook category polygons from IEM overlap where
# greater severe risk categories (i.e. 'HIGH') are found within lower
# severe risk categories (i.e. 'SLGT' or 'SLIGHT'). This python script
# removes the section of the lower risk category polygons which overlap
# with the higher risk polygons.
#
#
# BEFORE USING THIS SCRIPT, CHANGE THE FOLLOWING LINES:
# -Change the variable 'filepath' to the name of the downloaded shapefile
#
# -Change the name of the shapefile being written to in the 'with fiona.open...'
#  line to the correct filepath and name of the file you want. You may want
#  to use a naming convection similar to what's included in this original.
#
# -When writing out the new shapefile, the highest category being written out
#  (i.e. the highest category in the original shapefile) should be written
#  out as just [risk]_poly and not [risk]_hole_poly as the highest risk
#  category will not have a hole within it
#
# -Comment out any categories above the highest risk category in the shapefile
#  in the for loop, the *_poly* lines, and the with loop/c.write lines
#
# -Comment out the highest risk category in the *hole_poly* lines as the highest
#  risk category present does not need a hole
#
# -The 'TSTM' cateogry is likely to have multiple polygons as the lowest risk
#  category. check the number of separate 'TSTM' polygons either visually on
#  IEM or by writing out the 'TSTM' entry in the dict below, and comment out
#  any unnecessary lines in the tstm_hole_poly* lines. for example, if there
#  are 2 'TSTM' polygons, comment out the tstm_hole_poly3 and tstm_hole_poly4
#  lines and leave poly1 and poly2 uncommented. The with/c.write loop will
#  also need to be adjusted to write out the correct number of 'TSTM'
#  polygons. This original is formatted for the 2 'TSTM' polygons example as
#  described in this paragraph
#
#
# CAVEATS:
# -The SPC severe weather outlook shapefiles directly from the SPC archive
#  (NOT IEM) are already created with holes for the higher risk categories
#  and as such this code is not needed for those files. However, those files
#  directly from the SPC website do not necessarily have smooth edges for
#  outlooks within older years. This issue of smooth edges is resolved
#  with the IEM archive of SPC outlooks, hence the potential need for this
#  code.
#
# -The downloaded IEM severe category shapefile probably needs to have just one
#  complete outlook within it in order for this script to work, although this
#  hasn't been tested. The main reason for this is that different outlooks may
#  likely have different highest risk categories, which need to be specified
#  explicitly for this script to work.
#
# -See below for necessary packages: 'shapely', 'pyshp' (imported as
#  'shapefile'), and 'fiona'. Script was originally written and tested within
#  an Anaconda environment (version 4.10.3).
#
######################################################################################


from shapely.geometry import shape, Polygon, mapping
import shapefile
import fiona

filepath = 'C:/Users/bjig2/Documents/GIS/Projects/SPC_Severe/20150802/outlooks_201508021600_201508021700.shp'
shpfile = shapefile.Reader(filepath)
#print (shpfile.fields)
fields = shpfile.fields[1:]
field_names = [field[0] for field in fields]
for r in shpfile.shapeRecords():
	atr = dict(zip(field_names, r.record))
	#print (atr)
	print (r.record)
	print (r.record[5])
	if r.record[5] == 'TSTM':
		tstm_points = r.shape.points
	if r.record[5] == 'MRGL':
		mrgl_points = r.shape.points
	if r.record[5] == 'SLGT':
		slgt_points = r.shape.points
	if r.record[5] == 'ENH':
		enh_points = r.shape.points
#	if r.record[5] == 'MDT':
#		mdt_points = r.shape.points
#	if r.record[5] == 'HIGH':
#		high_points = r.shape.points

tstm_poly = Polygon(tstm_points)
mrgl_poly = Polygon(mrgl_points)
slgt_poly = Polygon(slgt_points)
enh_poly = Polygon(enh_points)
#mdt_poly = Polygon(mdt_points)
#high_poly = Polygon(high_points)

#feature13 = shpfile.shapeRecords()[12]
#print (feature13)
#tstm_points = feature13.shape.points
#tstm_poly = Polygon(tstm_points)

tstm_hole_collection = tstm_poly.difference(mrgl_poly)
tstm_hole_poly1 = tstm_hole_collection[0]
tstm_hole_poly2 = tstm_hole_collection[1]
#tstm_hole_poly3 = tstm_hole_collection[2]
#tstm_hole_poly4 = tstm_hole_collection[3]


mrgl_hole_poly = mrgl_poly.difference(slgt_poly)
slgt_hole_poly = slgt_poly.difference(enh_poly)
#enh_hole_poly = slgt_poly.difference(mdt_poly)
#mdt_hole_poly = slgt_poly.difference(high_poly)


schema = {
	'geometry': 'Polygon',
	'properties': {'THRESHOLD': 'str'},
}

with fiona.open('C:/Users/bjig2/Documents/GIS/Projects/SPC_Severe/20150802/newoutlook_20150802_1630Z.shp', 'w', 'ESRI Shapefile', schema) as c:
	c.write({
	'geometry': mapping(tstm_hole_poly1),
	'properties': {'THRESHOLD': 'TSTM'},
	})
	c.write({
	'geometry': mapping(tstm_hole_poly2),
	'properties': {'THRESHOLD': 'TSTM'},
	})
	c.write({
	'geometry': mapping(mrgl_hole_poly),
	'properties': {'THRESHOLD': 'MRGL'},
	})
	c.write({
	'geometry': mapping(slgt_hole_poly),
	'properties': {'THRESHOLD': 'SLGT'},
	})
	c.write({
	'geometry': mapping(enh_poly),
	'properties': {'THRESHOLD': 'ENH'},
	})
#	c.write({
#	'geometry': mapping(mdt_poly),
#	'properties': {'THRESHOLD': 'MDT'},
#	})
#	c.write({
#	'geometry': mapping(high_poly),
#	'properties': {'THRESHOLD': 'HIGH'},
#	})

