# Script Created by Tang Dynasty.
proc step_begin { step } {
  set stopFile ".stop.f"
  if {[file isfile .stop.f]} {
    puts ""
    puts " #Halting run"
    puts ""
    return -code error
  }
  set beginFile ".$step.begin.f"
  set platform "$::tcl_platform(platform)"
  set user "$::tcl_platform(user)"
  set pid [pid]
  set host ""
  if { [string equal $platform unix] } {
    if { [info exists ::env(HOSTNAME)] } {
      set host $::env(HOSTNAME)
    }
  } else {
    if { [info exists ::env(COMPUTERNAME)] } {
      set host $::env(COMPUTERNAME)
    }
  }
  set ch [open $beginFile w]
  puts $ch "<?xml version=\"1.0\"?>"
  puts $ch "<ProcessHandle Version=\"1\" Minor=\"0\">"
  puts $ch "    <Process Ownner=\"$user\" Host=\"$host\" Pid=\"$pid\">"
  puts $ch "    </Process>"
  puts $ch "</ProcessHandle>"
  close $ch
}
proc step_end { step } {
  set endFile ".$step.end.f"
  set ch [open $endFile w]
  close $ch
}
proc step_error { step } {
  set errorFile ".$step.error.f"
  set ch [open $errorFile w]
  close $ch
}
step_begin opt_place
set ACTIVESTEP opt_place
set rc [catch {
  import_device dr1_90.db -package DR1M90GEG484 -speed 2
  open_project {ov5640_udp_rgmii_8_8.prj} -noanalyze
  import_db {../syn_1/ov5640_udp_rgmii_8_8_gate.db}
  commit_param -step place
  place
  export_db {ov5640_udp_rgmii_8_8_place.db}
  update_timing -mode manhattan
  report_timing_summary -file ov5640_udp_rgmii_8_8_place.timing
} RESULT]
if {$rc} {
  step_error opt_place
  return -code error $RESULT
} else {
  step_end opt_place
  unset ACTIVESTEP
}
step_begin opt_route
set ACTIVESTEP opt_route
set rc [catch {
  commit_param -step route
  route
  report_area -io_info -file ov5640_udp_rgmii_8_8_phy.area
  export_db {ov5640_udp_rgmii_8_8_pr.db}
  update_timing -mode final
  report_timing_status -file ov5640_udp_rgmii_8_8_phy.ts
  report_timing_summary -file ov5640_udp_rgmii_8_8_pr.timing
  report_timing_exception -file ov5640_udp_rgmii_8_8_exception.timing
} RESULT]
if {$rc} {
  step_error opt_route
  return -code error $RESULT
} else {
  step_end opt_route
  unset ACTIVESTEP
}
step_begin bitgen
set ACTIVESTEP bitgen
set rc [catch {
  commit_param -step bitgen
  bitgen -bit "ov5640_udp_rgmii_8_8.bit"
} RESULT]
if {$rc} {
  step_error bitgen
  return -code error $RESULT
} else {
  step_end bitgen
  unset ACTIVESTEP
}
