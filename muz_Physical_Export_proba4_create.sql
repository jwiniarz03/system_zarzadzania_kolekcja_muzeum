-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-12-11 16:41:01.951

-- tables
-- Table: Artysta
CREATE TABLE Artysta (
    ID int  NOT NULL,
    imie varchar(20)  NOT NULL,
    nazwisko varchar(30)  NOT NULL,
    rok_urodzenia int  NOT NULL,
    rok_smierci int  NULL,
    CONSTRAINT Artysta_pk PRIMARY KEY (ID)
);

-- Table: Eksponat
CREATE TABLE Eksponat (
    ID int  NOT NULL,
    tytul varchar(50)  NULL,
    typ varchar(30)  NOT NULL,
    wysokosc numeric(10,3)  NOT NULL,
    szerokosc numeric(10,3)  NOT NULL,
    waga numeric(10,3)  NOT NULL,
    czy_najcenniejszy boolean  NOT NULL,
    Artysta_ID int  NULL,
    CONSTRAINT Eksponat_pk PRIMARY KEY (ID)
);

-- Table: Galeria
CREATE TABLE Galeria (
    Identyfikator int  NOT NULL,
    nazwa varchar(50)  NOT NULL,
    miasto varchar(40)  NOT NULL,
    CONSTRAINT Galeria_pk PRIMARY KEY (Identyfikator)
);

-- Table: Historia_magazynowania
CREATE TABLE Historia_magazynowania (
    ID serial  NOT NULL,
    data_rozpoczecia date  NOT NULL,
    data_zakonczenia date  NULL,
    cel varchar(40)  NOT NULL,
    Magazyn_Identyfikator int  NOT NULL,
    Eksponat_ID int  NOT NULL,
    CONSTRAINT Historia_magazynowania_pk PRIMARY KEY (ID)
);

-- Table: Historia_wypozyczen
CREATE TABLE Historia_wypozyczen (
    ID serial  NOT NULL,
    data_wypozyczenia date  NOT NULL,
    data_zwrotu date  NULL,
    Eksponat_ID int  NOT NULL,
    Instytucja_Identyfikator int  NOT NULL,
    CONSTRAINT Historia_wypozyczen_pk PRIMARY KEY (ID)
);

-- Table: Historia_wystaw
CREATE TABLE Historia_wystaw (
    ID serial  NOT NULL,
    data_rozpoczecia date  NOT NULL,
    data_zakonczenia date  NULL,
    nr_sali int  NOT NULL,
    Eksponat_ID int  NOT NULL,
    Galeria_Identyfikator int  NOT NULL,
    CONSTRAINT Historia_wystaw_pk PRIMARY KEY (ID)
);

-- Table: Instytucja
CREATE TABLE Instytucja (
    Identyfikator int  NOT NULL,
    nazwa varchar(50)  NOT NULL,
    miasto varchar(40)  NOT NULL,
    CONSTRAINT Instytucja_pk PRIMARY KEY (Identyfikator)
);

-- Table: Magazyn
CREATE TABLE Magazyn (
    Identyfikator int  NOT NULL,
    miasto varchar(40)  NOT NULL,
    CONSTRAINT Magazyn_pk PRIMARY KEY (Identyfikator)
);

-- foreign keys
-- Reference: Eksponat_Artysta (table: Eksponat)
ALTER TABLE Eksponat ADD CONSTRAINT Eksponat_Artysta
    FOREIGN KEY (Artysta_ID)
    REFERENCES Artysta (ID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Historia_magazynowania_Eksponat (table: Historia_magazynowania)
ALTER TABLE Historia_magazynowania ADD CONSTRAINT Historia_magazynowania_Eksponat
    FOREIGN KEY (Eksponat_ID)
    REFERENCES Eksponat (ID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Historia_magazynowania_Magazyn (table: Historia_magazynowania)
ALTER TABLE Historia_magazynowania ADD CONSTRAINT Historia_magazynowania_Magazyn
    FOREIGN KEY (Magazyn_Identyfikator)
    REFERENCES Magazyn (Identyfikator)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Historia_wypozyczen_Eksponat (table: Historia_wypozyczen)
ALTER TABLE Historia_wypozyczen ADD CONSTRAINT Historia_wypozyczen_Eksponat
    FOREIGN KEY (Eksponat_ID)
    REFERENCES Eksponat (ID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Historia_wypozyczen_Instytucja (table: Historia_wypozyczen)
ALTER TABLE Historia_wypozyczen ADD CONSTRAINT Historia_wypozyczen_Instytucja
    FOREIGN KEY (Instytucja_Identyfikator)
    REFERENCES Instytucja (Identyfikator)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Historia_wystaw_Eksponat (table: Historia_wystaw)
ALTER TABLE Historia_wystaw ADD CONSTRAINT Historia_wystaw_Eksponat
    FOREIGN KEY (Eksponat_ID)
    REFERENCES Eksponat (ID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Historia_wystaw_Galeria (table: Historia_wystaw)
ALTER TABLE Historia_wystaw ADD CONSTRAINT Historia_wystaw_Galeria
    FOREIGN KEY (Galeria_Identyfikator)
    REFERENCES Galeria (Identyfikator)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- sequences
-- Sequence: Artysta_seq
CREATE SEQUENCE Artysta_seq
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      START WITH 1
      NO CYCLE
;

-- Sequence: Eksponat_seq
CREATE SEQUENCE Eksponat_seq
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      START WITH 1
      NO CYCLE
;

-- Sequence: Galeria_seq
CREATE SEQUENCE Galeria_seq
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      START WITH 1
      NO CYCLE
;

-- Sequence: Historia_magazynowania_seq
CREATE SEQUENCE Historia_magazynowania_seq
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      START WITH 1
      NO CYCLE
;

-- Sequence: Historia_wypozyczen_seq
CREATE SEQUENCE Historia_wypozyczen_seq
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      START WITH 1
      NO CYCLE
;

-- Sequence: Historia_wystaw_seq
CREATE SEQUENCE Historia_wystaw_seq
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      START WITH 1
      NO CYCLE
;

-- Sequence: Instytucja_seq
CREATE SEQUENCE Instytucja_seq
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      START WITH 1
      NO CYCLE
;

-- Sequence: Magazyn_seq
CREATE SEQUENCE Magazyn_seq
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      START WITH 1
      NO CYCLE
;

-- End of file.

