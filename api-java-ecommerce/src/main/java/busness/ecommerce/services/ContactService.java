package busness.ecommerce.services;

import busness.ecommerce.dto.*;
import busness.ecommerce.enums.OrderStatus;

import java.util.List;

public interface ContactService {
    // POST
    ContactResponseDto createContact(ContactRequestDto dto);
    // READ
    List<ContactResponseDto> getAllContacts();
    // GET
    ContactResponseDto getContact(Long id);
    // GET
    List<ContactGroupByDateDto> getContactsGroupedByDate();
    // UPDATE
    ContactResponseDto updateContact(Long id, UpdateContactStatusRequestDto dto);
    // GET
    int getCountContactStatus(int status);
    // UPDATE
    int updateAllContactsStatus();
    // Delete
    void deleteContact(Long id);
}
