from datetime import datetime
from src.database.sqlite_wrapper import db as local_db
import sqlite3

class TransactionType:
    IN = "IN"
    OUT = "OUT"

class NoteStatus:
    IN = "IN"
    OUT = "OUT"

class TransactionService:
    def __init__(self, db_instance=None):
        # db_instance arg kept for backward compat signature, but we use local_db
        self.current_notes = {} # {serial: denomination}
        self.transaction_type = None

    def start_session(self, t_type):
        self.current_notes = {}
        self.transaction_type = t_type

    def scan_note(self, serial: str, denomination: int) -> dict:
        """
        Validates and adds a note to the current session.
        Returns: {'success': bool, 'message': str}
        """
        if serial in self.current_notes:
            return {'success': False, 'message': 'Note already scanned in this session'}

        conn = local_db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT status, denomination FROM notes WHERE serial_number = ?", (serial,))
            row = cursor.fetchone()
            
            existing_status = row[0] if row else None
            existing_denom = row[1] if row else None

            if self.transaction_type == TransactionType.IN:
                if existing_status == NoteStatus.IN:
                    return {'success': False, 'message': f'Note {serial} is already IN the system'}
            
            elif self.transaction_type == TransactionType.OUT:
                if not row:
                    return {'success': False, 'message': f'Note {serial} not found in system'}
                if existing_status == NoteStatus.OUT:
                    return {'success': False, 'message': f'Note {serial} is already OUT'}
                if existing_denom != denomination:
                     return {'success': False, 'message': f'Denomination mismatch for {serial}'}
            
            self.current_notes[serial] = denomination
            return {'success': True, 'message': f'Note {serial} accepted'}
            
        finally:
            conn.close()

    def commit_transaction(self, operator_id: int):
        if not self.current_notes:
            raise ValueError("No notes to commit")

        total_amount = sum(self.current_notes.values())
        timestamp = datetime.now()
        
        conn = local_db.get_connection()
        cursor = conn.cursor()
        
        try:
            # 1. Create Transaction Record
            cursor.execute('''
                INSERT INTO transactions (type, total_amount, operator_id, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (self.transaction_type, total_amount, operator_id, timestamp))
            
            # 2. Update Notes
            for serial, denom in self.current_notes.items():
                cursor.execute("SELECT serial_number FROM notes WHERE serial_number = ?", (serial,))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO notes (serial_number, denomination, status, last_seen, created_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (serial, denom, self.transaction_type, timestamp, timestamp))
                else:
                    cursor.execute('''
                        UPDATE notes SET status = ?, last_seen = ? WHERE serial_number = ?
                    ''', (self.transaction_type, timestamp, serial))
            
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_summary(self):
        return {
            'count': len(self.current_notes),
            'total': sum(self.current_notes.values())
        }
