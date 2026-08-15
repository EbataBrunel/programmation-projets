package eajc.group.apv.services;

import eajc.group.apv.dto.*;

import java.util.List;
import java.util.UUID;

public interface ContactService {
    // POST
    ContactResponseDto createContact(ContactRequestDto dto);
    // READ
    List<ContactResponseDto> getAllContacts();
    // GET
    ContactResponseDto getContact(UUID publicId);
    // GET
    List<ContactGroupByDateDto> getContactsGroupedByDate();
    // UPDATE
    ContactResponseDto updateContact(UUID publicId, UpdateContactStatusRequestDto dto);
    // GET
    int getCountContactStatus(int status);
    // UPDATE
    int updateAllContactsStatus();
    // Delete
    void deleteContact(UUID publicId);
}
