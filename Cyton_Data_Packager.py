# -*- coding: utf-8 -*-
"""
CruX UCLA 2023

@author: Darren Vawter

"""

import time;
import numpy as np;
from pyOpenBCI import OpenBCICyton;
from pylsl import StreamInfo, StreamOutlet;


#TODO: search for suspiciously large time gaps between samples
#TODO: check if any illegal trigger data is still being received

def Start():
          
    # The sampling rate of the Cyton board, in Hz
    sampling_rate = 250
        
    # Sample scaling    
    # SCALE_FACTOR_EEG = (4500000)/24/(2**23-1); #uV/count
    SCALE_FACTOR_EEG = (4500000)/12/(2**23-1); #uV/count
    SCALE_FACTOR_AUX = 0.002 / (2**4);
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    def Shutdown_Cyton_Data_Packager():
        
        print("Shutting down Cyton data packager...");
        
        ######################################
        #   Destroy the UM232R FTDI object   #
        ######################################
        
        try:
            
            print("Destroying Cyton's OpenBCICyton object...");
            
            if(cyton is not None):
                
                # Disconnect the Cyton to release the COM port
                cyton.disconnect();
                
            else:
                
                print("'cyton' is not defined.");
                
        except NameError:
            
            print("'cyton' is not declared.");
            
        except Exception as e:
            
            raise e;
                    
        ##############################
        #   Destroy the EEG outlet   #
        ##############################  
        
        try:
            
            print("Destroying EEG outlet...");
            
            if(stream_outlet is not None):
                
                # Send shutdown signal to any consumers of this outlet
                #TODO: define this
                Data_Packager_shutdown_signal = np.empty(9);
                
                # Wait for consumers to disconnect
                #TODO: consider setting a max timeout for this
                while(stream_outlet.have_consumers()):    
                    stream_outlet.push_sample(Data_Packager_shutdown_signal);         
                    # Wait for 100ms, then try again (instead of blocking)
                    # (this brief pause between calls allows for interrupts)
                    time.sleep(0.1);
                
                # Completely delete the stimuli outlet
                stream_outlet.__del__();
                
            else:
                
                print("'stream_outlet' is not defined.");
                
        except NameError:
            
            print("'stream_outlet' is not declared.");
            
        except Exception as e:
            
            raise e;
                         
        # End of Shutdown_Cyton_Data_Packager
        print("Cyton data packager shut down.");

        #TODO: remove
        try:
            
            while(True):
                time.sleep(.1);
                
        except KeyboardInterrupt:
            
            pass;
            
        pass;
    
    def Run():
        
        # The most recent EEG sample pulled from the Cyton
        current_sample_EEG = np.zeros([1,8]);
        
        # The most recent trigger sample pulled from the Cyton
        current_sample_trigger = np.zeros(1);
                           
        chunk_ind = 0;
        chunk = np.zeros((500,9));
        
        # Packages 1 sample of EEG/trigger data and adds it to the pending chunk
        def package_sample(sample):
                
            nonlocal current_sample_EEG, current_sample_trigger, chunk_ind
            
            res = np.zeros(9)
            
            # Pull sample from the 8 EEG channels
            current_sample_EEG = np.float32(np.array(sample.channels_data)*SCALE_FACTOR_EEG);            

            # Pull sample from the digital pins (this is a 1-byte value)
            current_sample_trigger = np.float32(sample.aux_data[1]-256)

            res[0:8] = current_sample_EEG;
            res[8] = current_sample_trigger;                                    
            chunk[chunk_ind,:] = res;
            
            chunk_ind += 1;
            if(chunk_ind==500):
                stream_outlet.push_chunk(chunk.tolist());         
                chunk_ind = 0;
                print("chunk sent")
                        
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#                       
        # Start the board stream with callback
        cyton.start_stream(package_sample);
            
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
    cyton = None;
    stream_outlet = None;
    
    try:
        
        # Connect to bluetooth dongle on COM port 3
        print("Connecting to Cyton...");
        cyton = OpenBCICyton(port='COM3');
                  
        # Configure the board into digital read mode
        print("Configuring Cyton...");
        cyton.write_command('/d');
        cyton.write_command("x1050110X")
        cyton.write_command("x2050110X")
        cyton.write_command("x3050110X")
        cyton.write_command("x4050110X")
        cyton.write_command("x5050110X")
        cyton.write_command("x6050110X")
        cyton.write_command("x7050110X")
        cyton.write_command("x8050110X")
        cyton.write_command('/3');
        print("Cyton ready.");
        
        # Initialize LSL stream
        print("Opening EEG outlet...");
        stream_info = StreamInfo("Packaged_EEG", "Packaged_EEG", 9, 250, "float32", "Cyton_Data_Packager");
        stream_outlet = StreamOutlet(stream_info);
        print("EEG outlet opened.");
    
        Run();
        
    except KeyboardInterrupt:
        
        print("Keyboard interrupt detected");
        Shutdown_Cyton_Data_Packager();
    
    except Exception as e:
        
        Shutdown_Cyton_Data_Packager();    
        raise e;
    
    else:
        
        Shutdown_Cyton_Data_Packager();
        
    finally:
        
        import sys;
        sys.exit(0);    
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#TODO: call this from a file that independently starts all 3 processes          
Start();  


















