##pysync

pysync is a tool written for me to manage my files on both my laptop and remotely. 

In general, it is often the case that I will have a large directory structure cloned locally, 
and I will edit parts of this structure both at home and at work at different times. I want an easy way to sync these two sets of files easily. rsync works great, but, it's a bit cumbersome sometimes to write the full paths out. Thus, instead of:

    #pull
    rsync -arvz user@host:<remote_path>/big_dir/.../working_dir  <local_path>/big_dir/.../working_dir
    #push
    rsync -arvz  <local_path>/big_dir/.../working_dir user@host:<remote_path>/big_dir/.../working_dir 

just do:

    #from <working_dir>
    pysync set_remote_path user@host:<remote_path>/big_dir/.../working_dir
    pysync pull
    pysync push

there's not much to it, but, for me I'd always make tiny errors in my full push or pull rsync which would totally screw me. This helps
