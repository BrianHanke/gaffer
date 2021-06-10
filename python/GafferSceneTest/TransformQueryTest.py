##########################################################################
#
#  Copyright (c) 2021, Cinesite VFX Ltd. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import unittest
import imath

import IECore

import Gaffer
import GafferScene
import GafferSceneTest

class TransformQueryTest( GafferSceneTest.SceneTestCase ):

	def testOutMatrix( self ):

		from random import Random
		from datetime import datetime

		s1 = GafferScene.Sphere()
		s2 = GafferScene.Sphere()
		gr = GafferScene.Group()
		tq = GafferScene.TransformQuery()

		gr["in"][0].setInput( s1["out"] )
		gr["in"][1].setInput( s2["out"] )
		tq["scene"].setInput( gr["out"] )

		s1["name"].setValue( "sphere1" )
		s2["name"].setValue( "sphere2" )
		gr["name"].setValue( "group" )

		r = Random( datetime.now() )

		s1t = imath.V3f(
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0 )

		s2t = imath.V3f(
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0 )

		grt = imath.V3f(
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0 )

		s1r = imath.V3f(
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0 )

		s2r = imath.V3f(
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0 )

		grr = imath.V3f(
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0 )

		s1s = imath.V3f(
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ) )

		s2s = imath.V3f(
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ) )

		grs = imath.V3f(
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ) )

		s1["transform"]["translate"].setValue( s1t )
		s1["transform"]["rotate"].setValue( s1r )
		s1["transform"]["scale"].setValue( s1s )
		s1m = s1["transform"].matrix()

		s2["transform"]["translate"].setValue( s2t )
		s2["transform"]["rotate"].setValue( s2r )
		s2["transform"]["scale"].setValue( s2s )
		s2m = s2["transform"].matrix()

		gr["transform"]["translate"].setValue( grt )
		gr["transform"]["rotate"].setValue( grr )
		gr["transform"]["scale"].setValue( grs )
		grm = gr["transform"].matrix()

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Local )

		m = s1m
		self.assertTrue( tq["outMatrix"].getValue().equalWithAbsError( m, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Local )

		m = s1m.inverse()
		self.assertTrue( tq["outMatrix"].getValue().equalWithAbsError( m, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.World )

		m = ( s1m * grm )
		self.assertTrue( tq["outMatrix"].getValue().equalWithAbsError( m, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.World )

		m = ( s1m * grm ).inverse()
		self.assertTrue( tq["outMatrix"].getValue().equalWithAbsError( m, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["relativeLocation"].setValue( "/group/sphere2" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Relative )

		m = ( s1m * grm ) * ( s2m * grm ).inverse()
		self.assertTrue( tq["outMatrix"].getValue().equalWithAbsError( m, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["relativeLocation"].setValue( "/group/sphere2" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Relative )

		m = ( ( s1m * grm ) * ( s2m * grm ).inverse() ).inverse()
		self.assertTrue( tq["outMatrix"].getValue().equalWithAbsError( m, 0.000001 ) )

	def testOutTranslate( self ):

		from random import Random
		from datetime import datetime

		s1 = GafferScene.Sphere()
		s2 = GafferScene.Sphere()
		gr = GafferScene.Group()
		tq = GafferScene.TransformQuery()

		gr["in"][0].setInput( s1["out"] )
		gr["in"][1].setInput( s2["out"] )
		tq["scene"].setInput( gr["out"] )

		s1["name"].setValue( "sphere1" )
		s2["name"].setValue( "sphere2" )
		gr["name"].setValue( "group" )

		r = Random( datetime.now() )

		s1t = imath.V3f(
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0 )

		s2t = imath.V3f(
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0 )

		grt = imath.V3f(
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0,
			( r.random() - 0.5 ) * 2.0 )

		s1["transform"]["translate"].setValue( s1t )
		s1m = s1["transform"].matrix()

		s2["transform"]["translate"].setValue( s2t )
		s2m = s2["transform"].matrix()

		gr["transform"]["translate"].setValue( grt )
		grm = gr["transform"].matrix()

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Local )

		v = s1m.translation()
		self.assertTrue( tq["outTranslate"].getValue().equalWithAbsError( v, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Local )

		v = s1m.inverse().translation()
		self.assertTrue( tq["outTranslate"].getValue().equalWithAbsError( v, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.World )

		v = ( s1m * grm ).translation()
		self.assertTrue( tq["outTranslate"].getValue().equalWithAbsError( v, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.World )

		v = ( s1m * grm ).inverse().translation()
		self.assertTrue( tq["outTranslate"].getValue().equalWithAbsError( v, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["relativeLocation"].setValue( "/group/sphere2" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Relative )

		v = ( ( s1m * grm ) * ( s2m * grm ).inverse() ).translation()
		self.assertTrue( tq["outTranslate"].getValue().equalWithAbsError( v, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["relativeLocation"].setValue( "/group/sphere2" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Relative )

		v = ( ( s1m * grm ) * ( s2m * grm ).inverse() ).inverse().translation()
		self.assertTrue( tq["outTranslate"].getValue().equalWithAbsError( v, 0.000001 ) )

	def testOutRotate( self ):

		from math import pi
		from random import Random
		from datetime import datetime

		s1 = GafferScene.Sphere()
		s2 = GafferScene.Sphere()
		gr = GafferScene.Group()
		tq = GafferScene.TransformQuery()

		gr["in"][0].setInput( s1["out"] )
		gr["in"][1].setInput( s2["out"] )
		tq["scene"].setInput( gr["out"] )

		s1["name"].setValue( "sphere1" )
		s2["name"].setValue( "sphere2" )
		gr["name"].setValue( "group" )

		r = Random( datetime.now() )

		s1r = imath.V3f(
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0 )

		s2r = imath.V3f(
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0 )

		grr = imath.V3f(
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0,
			( r.random() - 0.5 ) * 2.0 * 180.0 )

		s1["transform"]["rotate"].setValue( s1r )
		s1m = s1["transform"].matrix()

		s2["transform"]["rotate"].setValue( s2r )
		s2m = s2["transform"].matrix()

		gr["transform"]["rotate"].setValue( grr )
		grm = gr["transform"].matrix()

		ro = imath.Eulerf.XYZ

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Local )

		m = s1m
		e = imath.Eulerf( imath.M44f.sansScalingAndShear( m ), ro ) * ( 180.0 / pi )
		self.assertTrue( tq["outRotate"].getValue().equalWithAbsError( e, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Local )

		m = s1m.inverse()
		e = imath.Eulerf( imath.M44f.sansScalingAndShear( m ), ro ) * ( 180.0 / pi )
		self.assertTrue( tq["outRotate"].getValue().equalWithAbsError( e, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.World )

		m = ( s1m * grm )
		e = imath.Eulerf( imath.M44f.sansScalingAndShear( m ), ro ) * ( 180.0 / pi )
		self.assertTrue( tq["outRotate"].getValue().equalWithAbsError( e, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.World )

		m = ( s1m * grm ).inverse()
		e = imath.Eulerf( imath.M44f.sansScalingAndShear( m ), ro ) * ( 180.0 / pi )
		self.assertTrue( tq["outRotate"].getValue().equalWithAbsError( e, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["relativeLocation"].setValue( "/group/sphere2" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Relative )

		m = ( s1m * grm ) * ( s2m * grm ).inverse()
		e = imath.Eulerf( imath.M44f.sansScalingAndShear( m ), ro ) * ( 180.0 / pi )
		self.assertTrue( tq["outRotate"].getValue().equalWithAbsError( e, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["relativeLocation"].setValue( "/group/sphere2" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Relative )

		m = ( ( s1m * grm ) * ( s2m * grm ).inverse() ).inverse()
		e = imath.Eulerf( imath.M44f.sansScalingAndShear( m ), ro ) * ( 180.0 / pi )
		self.assertTrue( tq["outRotate"].getValue().equalWithAbsError( e, 0.000001 ) )

	def testOutScale( self ):

		from random import Random
		from datetime import datetime

		s1 = GafferScene.Sphere()
		s2 = GafferScene.Sphere()
		gr = GafferScene.Group()
		tq = GafferScene.TransformQuery()

		gr["in"][0].setInput( s1["out"] )
		gr["in"][1].setInput( s2["out"] )
		tq["scene"].setInput( gr["out"] )

		s1["name"].setValue( "sphere1" )
		s2["name"].setValue( "sphere2" )
		gr["name"].setValue( "group" )

		r = Random( datetime.now() )

		s1s = imath.V3f(
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ) )

		s2s = imath.V3f(
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ) )

		grs = imath.V3f(
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ),
			( r.random()         * 2.0 ) )

		s1["transform"]["scale"].setValue( s1s )
		s1m = s1["transform"].matrix()

		s2["transform"]["scale"].setValue( s2s )
		s2m = s2["transform"].matrix()

		gr["transform"]["scale"].setValue( grs )
		grm = gr["transform"].matrix()

		s = imath.V3f()

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Local )

		m = s1m
		imath.M44f.extractScaling( m, s )
		self.assertTrue( tq["outScale"].getValue().equalWithAbsError( s, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Local )

		m = s1m.inverse()
		imath.M44f.extractScaling( m, s )
		self.assertTrue( tq["outScale"].getValue().equalWithAbsError( s, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.World )

		m = ( s1m * grm )
		imath.M44f.extractScaling( m, s )
		self.assertTrue( tq["outScale"].getValue().equalWithAbsError( s, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.World )

		m = ( s1m * grm ).inverse()
		imath.M44f.extractScaling( m, s )
		self.assertTrue( tq["outScale"].getValue().equalWithAbsError( s, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["relativeLocation"].setValue( "/group/sphere2" )
		tq["invert"].setValue( False )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Relative )

		m = ( s2m * grm ).inverse() * ( s1m * grm )
		imath.M44f.extractScaling( m, s )
		self.assertTrue( tq["outScale"].getValue().equalWithAbsError( s, 0.000001 ) )

		tq["location"].setValue( "/group/sphere1" )
		tq["relativeLocation"].setValue( "/group/sphere2" )
		tq["invert"].setValue( True )
		tq["space"].setValue( GafferScene.TransformQuery.Space.Relative )

		m = ( ( s2m * grm ).inverse() * ( s1m * grm ) ).inverse()
		imath.M44f.extractScaling( m, s )
		self.assertTrue( tq["outScale"].getValue().equalWithAbsError( s, 0.000001 ) )

if __name__ == "__main__":
	unittest.main()