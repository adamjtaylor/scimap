# -*- coding: utf-8 -*-
# Created on Mon Nov  9 21:00:57 2020
# @author: Ajit Johnson Nirmal
"""
!!! abstract "Short Description"
    `sm.hl.scimap_to_csv`:  Helper function that allows users to save the contents of the `scimap` object as a csv file.
    Please not that anything that it only saves elements that are within `adata.X or adata.raw.X ` and `adata.obs`.

## Function
"""

# Import
import pandas as pd
import numpy as np
import argparse
import sys
import pathlib
import anndata as ad


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(
        description='Helper function that allows users to save the contents of the `scimap` object as a csv file.'
    )
    parser.add_argument(
        '--adata', required=True, 
        help='AnnData object loaded into memory or path to AnnData object.'
    )
    parser.add_argument(
        '--data_type', type=str, required=False, default='raw',
        help='Three options are available: 1) `raw` - The raw data will be returned; 2) `log` - The raw data converted to log scale using `np.log1p` will be returned; 3) `scaled` - If you have scaled the data using the `sm.pp.rescale`, that will be returned. Please note, if you have not scaled the data, whatever is within `adata.X` will be returned'
    )
    parser.add_argument(
        '--output_dir', type=str, required=False, default=None,
        help='Path to output directory.'
    )
    parser.add_argument(
        '--file_name', type=str, required=False, default=None,
        help='Name the output csv file. Use in combination with `output_dir` parameter. If no file name is provided a default name `scimap_to_csv_file.csv` will be used. '
    )
    parser.add_argument(
        '--CellID', type=str, required=False, default='CellID',
        help='Name of the column which contains the CellID.'
    )
    args = parser.parse_args(argv[1:])
    print(vars(args))
    scimap_to_csv(**vars(args))
    

# Function
def scimap_to_csv (adata, data_type='raw', output_dir=None, file_name=None, CellID='CellID'):
    """
Parameters:
    adata : AnnData object loaded into memory or path to AnnData object.

    data_type (string):  
        Three options are available:  
        1) 'raw' - The raw data will be returned.  
        2) 'log' - The raw data converted to log scale using `np.log1p` will be returned.  
        3) 'scaled' - If you have scaled the data using the `sm.pp.rescale`, that will be
        returned. Please note, if you have not scaled the data, whatever is within
        `adata.X` will be returned.
        
    output_dir (string):  
        Path to output directory.
    
    file_name (string):  
        Name the output csv file. Use in combination with `output_dir` parameter. If no
        file name is provided a default name `scimap_to_csv_file.csv` will be used. 
    
    CellID (string):  
        Name of the column which contains the CellID. Default is `CellID`.  

Returns:
    merged (DataFrame):  
        A single dataframe containing the expression and metadata will be returned.
        
Example:
```python
    data = sm.hl.scimap_to_csv (adata, data_type='raw')
```
    """
    
    # Load the andata object    
    if isinstance(adata, str):
        if file_name is None:
            imid = str(adata.rsplit('/', 1)[-1])
        else: 
            imid = str(file_name)
        adata = ad.read(adata)
    else:
        if file_name is None:
            imid = "scimap_to_csv_file.csv"
        else: 
            imid = str(file_name)
        adata = adata
    
    # Expression matrix
    if data_type == 'raw':
        data = pd.DataFrame(adata.raw.X, index=adata.obs.index, columns=adata.var.index)
    if data_type == 'log':
        data = pd.DataFrame(np.log1p(adata.raw.X), index=adata.obs.index, columns=adata.var.index)
    if data_type == 'scaled':
        data = pd.DataFrame(adata.X, index=adata.obs.index, columns=adata.var.index)
    
    # Metadata
    meta = pd.DataFrame(adata.obs)
    
    # Merge the two dataframes
    merged = pd.concat([data, meta], axis=1, sort=False)
        
    # Add a column to save cell-id
    #merged['CellID'] = merged.index
    # make cellID the first column
    if CellID in merged.columns:
        first_column = merged.pop(CellID)
        merged.insert(0, CellID, first_column)
    else:
        merged['CellID'] = merged.index
        first_column = merged.pop(CellID)
        merged.insert(0, CellID, first_column)
    
    # reset index
    merged = merged.reset_index(drop=True)

    # Save data if requested
    if output_dir is not None:
        output_dir = pathlib.Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        merged.to_csv(output_dir / f'{imid}.csv', index=False)
    else:    
        # Return data
        return merged

if __name__ == '__main__':
    main()

