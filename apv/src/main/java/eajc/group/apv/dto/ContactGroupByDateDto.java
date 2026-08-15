package eajc.group.apv.dto;

import eajc.group.apv.entity.Contact;

import java.time.LocalDate;
import java.util.List;


public class ContactGroupByDateDto {
    private LocalDate date;
    private List<Contact> contacts;

    public ContactGroupByDateDto(){}

    public ContactGroupByDateDto(LocalDate date, List<Contact> contacts) {
        this.date = date;
        this.contacts = contacts;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public List<Contact> getContacts() {
        return contacts;
    }

    public void setContacts(List<Contact> contacts) {
        this.contacts = contacts;
    }
}
