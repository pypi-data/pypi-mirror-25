Classical PSHA with non-trivial logic tree (1 source model + 5 (a, b) pairs per source + 3 Mmax per source
==========================================================================================================

==================================================== ========================
tstation.gem.lan:/home/michele/oqdata/calc_5537.hdf5 Fri Sep 22 11:29:45 2017
checksum32                                           1,751,642,476           
engine_version                                       2.6.0-gite59d75a        
==================================================== ========================

num_sites = 1, num_imts = 1

Parameters
----------
=============================== ==================
calculation_mode                'classical'       
number_of_logic_tree_samples    10                
maximum_distance                {'default': 200.0}
investigation_time              50.0              
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            2.0               
complex_fault_mesh_spacing      2.0               
width_of_mfd_bin                0.1               
area_source_discretization      10.0              
ground_motion_correlation_model None              
random_seed                     23                
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source                  `source_model.xml <source_model.xml>`_                      
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
============================================= ====== ====================================== =============== ================
smlt_path                                     weight source_model_file                      gsim_logic_tree num_realizations
============================================= ====== ====================================== =============== ================
b11_b20_b31_b43_b52_b62_b72_b82_b91_b103_b112 0.100  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
b11_b21_b32_b43_b52_b62_b72_b82_b92_b102_b112 0.100  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
b11_b21_b32_b43_b52_b62_b73_b82_b92_b103_b113 0.100  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
b11_b22_b31_b43_b52_b64_b73_b84_b92_b104_b112 0.100  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
b11_b22_b32_b42_b51_b61_b72_b83_b91_b101_b111 0.100  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
b11_b22_b32_b42_b53_b62_b72_b81_b92_b103_b112 0.100  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
b11_b22_b33_b42_b52_b62_b72_b82_b92_b100_b112 0.100  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
b11_b23_b32_b43_b52_b62_b73_b82_b93_b101_b113 0.100  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
b11_b24_b32_b41_b51_b62_b71_b84_b93_b101_b111 0.100  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
b11_b24_b33_b40_b52_b62_b72_b81_b91_b102_b112 0.100  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
============================================= ====== ====================================== =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== =================== ========= ========== ==========
grp_id gsims               distances siteparams ruptparams
====== =================== ========= ========== ==========
0      BooreAtkinson2008() rjb       vs30       mag rake  
1      BooreAtkinson2008() rjb       vs30       mag rake  
2      BooreAtkinson2008() rjb       vs30       mag rake  
3      BooreAtkinson2008() rjb       vs30       mag rake  
4      BooreAtkinson2008() rjb       vs30       mag rake  
5      BooreAtkinson2008() rjb       vs30       mag rake  
6      BooreAtkinson2008() rjb       vs30       mag rake  
7      BooreAtkinson2008() rjb       vs30       mag rake  
8      BooreAtkinson2008() rjb       vs30       mag rake  
9      BooreAtkinson2008() rjb       vs30       mag rake  
====== =================== ========= ========== ==========

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=10, rlzs=10)
  0,BooreAtkinson2008(): [0]
  1,BooreAtkinson2008(): [1]
  2,BooreAtkinson2008(): [2]
  3,BooreAtkinson2008(): [3]
  4,BooreAtkinson2008(): [4]
  5,BooreAtkinson2008(): [5]
  6,BooreAtkinson2008(): [6]
  7,BooreAtkinson2008(): [7]
  8,BooreAtkinson2008(): [8]
  9,BooreAtkinson2008(): [9]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== =========== ============ ============
source_model     grp_id trt                  num_sources eff_ruptures tot_ruptures
================ ====== ==================== =========== ============ ============
source_model.xml 0      Active Shallow Crust 5           1925         1,925       
source_model.xml 1      Active Shallow Crust 5           2025         2,025       
source_model.xml 2      Active Shallow Crust 5           2135         2,135       
source_model.xml 3      Active Shallow Crust 5           2035         2,035       
source_model.xml 4      Active Shallow Crust 5           1865         1,865       
source_model.xml 5      Active Shallow Crust 5           2085         2,085       
source_model.xml 6      Active Shallow Crust 5           2075         2,075       
source_model.xml 7      Active Shallow Crust 5           2185         2,185       
source_model.xml 8      Active Shallow Crust 5           1905         1,905       
source_model.xml 9      Active Shallow Crust 5           2025         2,025       
================ ====== ==================== =========== ============ ============

============= ======
#TRT models   10    
#sources      50    
#eff_ruptures 20,260
#tot_ruptures 20,260
#tot_weight   0     
============= ======

Informational data
------------------
=========================== ====================================================================================
count_eff_ruptures.received tot 10.96 KB, max_per_task 716 B                                                    
count_eff_ruptures.sent     sources 56.78 KB, srcfilter 11.36 KB, param 10.03 KB, monitor 5.43 KB, gsims 1.69 KB
hazard.input_weight         2026.0                                                                              
hazard.n_imts               1                                                                                   
hazard.n_levels             3                                                                                   
hazard.n_realizations       10                                                                                  
hazard.n_sites              1                                                                                   
hazard.n_sources            50                                                                                  
hazard.output_weight        9.0                                                                                 
hostname                    tstation.gem.lan                                                                    
require_epsilons            False                                                                               
=========================== ====================================================================================

Slowest sources
---------------
====== ========= ============ ============ ========= ========= =========
grp_id source_id source_class num_ruptures calc_time num_sites num_split
====== ========= ============ ============ ========= ========= =========
5      5         AreaSource   375          0.002     1         1        
3      1         AreaSource   325          0.001     1         1        
1      5         AreaSource   375          0.001     1         1        
3      5         AreaSource   375          0.001     1         1        
1      1         AreaSource   375          0.001     1         1        
7      1         AreaSource   375          0.001     1         1        
0      1         AreaSource   325          0.001     1         1        
5      1         AreaSource   375          0.001     1         1        
8      1         AreaSource   375          0.001     1         1        
7      5         AreaSource   425          0.001     1         1        
5      2         AreaSource   510          0.001     1         1        
4      4         AreaSource   325          0.001     1         1        
3      3         AreaSource   510          0.001     1         1        
8      2         AreaSource   390          0.001     1         1        
0      5         AreaSource   375          0.001     1         1        
1      4         AreaSource   375          0.001     1         1        
2      4         AreaSource   375          0.001     1         1        
7      4         AreaSource   425          0.001     1         1        
1      2         AreaSource   450          0.001     1         1        
7      2         AreaSource   450          0.001     1         1        
====== ========= ============ ============ ========= ========= =========

Computation times by source typology
------------------------------------
============ ========= ======
source_class calc_time counts
============ ========= ======
AreaSource   0.063     50    
============ ========= ======

Duplicated sources
------------------
========= ========= ===================
source_id calc_time src_group_ids      
========= ========= ===================
1         0.013     0 1 2 3 4 5 6 7 8 9
2         0.012     0 1 2 3 4 5 6 7 8 9
3         0.012     0 1 2 3 4 5 6 7 8 9
4         0.012     0 1 2 3 4 5 6 7 8 9
5         0.013     0 1 2 3 4 5 6 7 8 9
========= ========= ===================
Sources with the same ID but different parameters

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
count_eff_ruptures 0.005 0.002  0.002 0.008 17       
================== ===== ====== ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
reading composite source model 0.229     0.0       1     
total count_eff_ruptures       0.079     0.0       17    
prefiltering source model      0.032     0.0       1     
managing sources               0.025     0.0       1     
store source_info              0.006     0.0       1     
aggregate curves               4.032E-04 0.0       17    
reading site collection        4.792E-05 0.0       1     
saving probability maps        3.099E-05 0.0       1     
============================== ========= ========= ======