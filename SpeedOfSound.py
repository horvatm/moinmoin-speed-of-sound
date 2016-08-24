"""
    MoinMoin  - SoundOfSpeed  Macro

    @copyright: 2015 by Martin Horvat (martin.horvat@fmf.uni-lj.si)
    
    @license:   GNU GPL, see COPYING for details

    Usage: 
    << SpeedOfSound()>>
    
    << SpeedOfSound(temperature, pressure, relative_humidity)>>
    
    History:
    - 2015.05.24: written by Martin Horvat for MoinMoin 1.9
     
"""

from MoinMoin import wikiutil
from MoinMoin.parser.text_moin_wiki import Parser as WikiParser


def macro_SpeedOfSound(macro, temperature=20.0, pressure=101.325, relative_humidity=0.0):
   
  return '''
  <style type="text/css">
  .speedofsound {
    border: 0px;
  }
  .speedofsound td{
    border: 0px;
    height: 1em;
  }
  </style>
   
  <table class="speedofsound">
  <tr> 
   <td>Temperature: </td> 
   <td> 
     <input type="number" id="temp" value="%1.3f" min="-273.15" step="0.01" onchange="speedofsound()"> [&#8451;] 
  </td> 
  </tr>
  <tr> 
   <td> Pressure: </td>
   <td>
     <input type="number" id="pres" value="%1.3f" min="0" step="0.01" onchange="speedofsound()"> [kPa] 
  </td> 
  </tr>
  <tr> 
   <td> Relative Humidity: </td>
   <td>
     <input type="number" id="rhum" value="%1.3f" min="0" max="100" step="0.01" onchange="speedofsound()"> [&#37;] 
   </td> 
  </tr>
  <tr> <td></td> </tr>
  <tr> 
   <td> Speed of sound:</td>
   <td>
     <input type="number" id="speed" value=0 readonly> [m/s]
   </td>
  </tr>
  </table>
   
  <script type="text/javascript">
  
  // function to round x to dp decimal places
  function roundto(x,dp){return (Math.round(x*Math.pow(10,dp))/Math.pow(10,dp));}

  function sqr(x){return  Math.pow(x,2);}

  // The calculator presented here computes the zero-frequency speed 
  // of sound in humid air according to Cramer (J. Acoust. Soc. Am., 93, p2510, 1993),
  // with saturation vapour pressure taken from Davis, Metrologia, 29, p67, 1992, 
  // and a mole fraction of carbon dioxide of 0.0004.

  function speedofsound() {
  
    var T = parseFloat(document.getElementById("temp").value); // temperature degC
    var P = parseFloat(document.getElementById("pres").value)*1000.0; // pressure in kPa
    var Rh = parseFloat(document.getElementById("rhum").value); // relative humidity

    var C;        // speed
    var Xc, Xw;   // Mole fraction of carbon dioxide and water vapour respectively
    var H;        // molecular concentration of water vapour

    var C1;       // Intermediate calculations
    var C2;
    var C3;

    var ENH;
    var PSV;
    var PSV1;
    var PSV2;

    var T_kel = 273.15 + T;    // ambient temperature (Kelvin)

    //Molecular concentration of water vapour calculated from Rh
    //using Giacomos method by Davis (1991) as implemented in DTU report 11b-1997
    ENH = 3.14e-8*P + 1.00062 + sqr(T)*5.6e-7;
    
    PSV1 = sqr(T_kel)*1.2378847e-5 - 1.9121316e-2*T_kel;
    PSV2 = 33.93711047 - 6.3431645e3/T_kel;
    PSV = Math.exp(PSV1)*Math.exp(PSV2);
    H = Rh*ENH*PSV/P;
    Xw = H/100.0;
    Xc = 400.0e-6;

    //Speed calculated using the method of Cramer from JASA vol 93 pg 2510
    C1 = 0.603055*T + 331.5024 - sqr(T)*5.28e-4 + (0.1495874*T + 51.471935 -sqr(T)*7.82e-4)*Xw;
    C2 = (-1.82e-7 + 3.73e-8*T - sqr(T)*2.93e-10)*P + (-85.20931-0.228525*T+sqr(T)*5.91e-5)*Xc;
    C3 = sqr(Xw)*2.835149 + sqr(P)*2.15e-13 - sqr(Xc)*29.179762 - 4.86e-4*Xw*P*Xc;
    C = C1 + C2 - C3;

    document.getElementById("speed").value =  roundto(C,3);
  }

  speedofsound();   
  </script> ''' % (temperature, pressure, relative_humidity)
