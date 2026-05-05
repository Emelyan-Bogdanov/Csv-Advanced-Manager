import csv
from pathlib import Path
from typing import Dict, List, Any


def read_csv_file(file_path: str) -> Dict[str, Any]:
    """
    Read a CSV file and return formatted data for Jinja2 templates.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        Dict containing:
            - 'headers': List of column names
            - 'rows': List of dictionaries (each row as a dict)
            - 'rows_list': List of lists (each row as a list)
            - 'total_rows': Total number of data rows
            - 'success': Boolean indicating if read was successful
            - 'error': Error message if failed (None if successful)
            - 'filename': Name of the file
    """
    result = {
        'headers': [],
        'rows': [],
        'rows_list': [],
        'total_rows': 0,
        'success': False,
        'error': None,
        'filename': ''
    }
    
    try:
        path = Path(file_path)
        
        # Validate file exists
        if not path.exists():
            result['error'] = f"File not found: {file_path}"
            return result
        
        # Validate it's a CSV file
        if path.suffix.lower() != '.csv':
            result['error'] = f"File must be a CSV file, got: {path.suffix}"
            return result
        
        result['filename'] = path.name
        
        # Read the CSV file
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Get headers
            if reader.fieldnames:
                result['headers'] = list(reader.fieldnames)
            else:
                result['error'] = "CSV file has no headers"
                return result
            
            # Read all rows
            for row in reader:
                result['rows'].append(row)
                result['rows_list'].append([row.get(header, '') for header in result['headers']])
        
        result['total_rows'] = len(result['rows'])
        result['success'] = True
        
    except UnicodeDecodeError:
        result['error'] = "Unable to decode file. Try a different encoding or ensure file is UTF-8."
    except csv.Error as e:
        result['error'] = f"CSV parsing error: {str(e)}"
    except Exception as e:
        result['error'] = f"Unexpected error: {str(e)}"
    
    return result


def read_csv_file_paginated(file_path: str, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """
    Read a CSV file and return paginated data for Jinja2 templates.
    
    Args:
        file_path (str): Path to the CSV file
        page (int): Page number (1-indexed)
        per_page (int): Number of rows per page
        
    Returns:
        Dict containing:
            - 'headers': List of column names
            - 'rows': List of dictionaries for current page
            - 'total_rows': Total number of data rows
            - 'total_pages': Total number of pages
            - 'current_page': Current page number
            - 'per_page': Rows per page
            - 'has_next': Boolean if next page exists
            - 'has_prev': Boolean if previous page exists
            - 'success': Boolean indicating if read was successful
            - 'error': Error message if failed
            - 'filename': Name of the file
    """
    # First read all data
    data = read_csv_file(file_path)
    
    if not data['success']:
        return data
    
    # Add pagination info
    total_rows = data['total_rows']
    total_pages = (total_rows + per_page - 1) // per_page  # Ceiling division
    
    # Validate page number
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    
    # Calculate slice indices
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # Add pagination data
    data['rows'] = data['rows'][start_idx:end_idx]
    data['total_pages'] = total_pages
    data['current_page'] = page
    data['per_page'] = per_page
    data['has_next'] = page < total_pages
    data['has_prev'] = page > 1
    
    return data