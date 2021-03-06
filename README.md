# iotdb-vocabulary
## Introduction

This is the iotdb.org vocabulary for describing Things -
Sensors and Actuators - in the Internet of Things.

If you make changes, push them back to us. 

## Schema.org

We've moved from using iot: names to schema.org names
from [Thing](http://schema.org/Thing). Specifically

* additionalType  
* alternateName  
* name    
* description 
* image   
* sameAs  
* url

## Structure

### src

The source files are in "src". The hierarchical structure of 
the folders is:

* iot-unit|iot-facet|iot-placement|iot
* @type
* @id (in particular, the part after #) - a file

The files are a simple text format, a
key followed by a space followed by a value.
Keys may repeat multiple times

e.g.

    description when to end / finish something
    format iot:date
    format iot:time
    format iot:datetime

the <code>schema:name</code>, <code>@type</code> and <code>@id</code>
are automatically made by the DoCompose function.

### pub

The "published" JSON-LD files are folder `pub`. Note that
the **official** URL home for these is 
[https://iotdb.org/pub](https://iotdb.org/pub), not the GitHub
folder.

To generate the JSON-LD files from the source files, run:

	npm run publish

The program <code>bin/DoCompose.py</code> converts
the files in <code>src</code> to JSON-LD in this 
directory.

## Making changes

* Fork this project
* Add whatever to src/iot-[something]/[@type]/[name]  (See Units of Measure below for rules specific to that)
* Commit
* Push

If accepted, they will be officially published
at [https://iotdb.org/pub](https://iotdb.org/pub)

## Units of Measure

The Units of Measure are in <code>iot-unit.jsonld</code>
from the directory <code>src/iot-unit/Unit</code>

Each unit of measure filename must have three parts, separated
by '.':

* the _property_
* the _system_
* the _name_

The property is very loosey-goosey and is meant for _humans_
to read and understand and is based on colloquial understandings
of a word rather than a formal defintion. For example, speed and
acceleration are grouped together under "speed"; 
candela, lux and lumen are grouped together under "light".

The property **must** be one of the following:

* area
* energy
* length
* light
* mass
* math
* pressure
* radioactivity
* speed
* temperature
* time
* volume

The _system_ **must** be one of the following

* angle
* constant
* fraction
* imperial
* si
* traditional
* troy
* us

The name is exactly what you'd expect.

### Adding New Units of Measure

Important:

* following the three part convention
* do not add new things unless you're planning to use it
* try not add SI multiplier units (e.g. centigram) unless
they're very commonly used. Exponents can be added
to values if this is needed.
