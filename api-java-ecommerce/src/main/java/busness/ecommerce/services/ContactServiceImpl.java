package busness.ecommerce.services;

import busness.ecommerce.dto.*;
import busness.ecommerce.entity.Contact;
import busness.ecommerce.mapper.ContactMapper;
import busness.ecommerce.repository.ContactRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional
public class ContactServiceImpl implements ContactService{

    private final ContactRepository contactRepository;
    private final ContactMapper contactMapper;
    @Override
    public ContactResponseDto createContact(ContactRequestDto dto) {
        Contact contact = contactMapper.toEntity(dto);
        Contact contactSave = contactRepository.save(contact);

        return contactMapper.toDto(contactSave);
    }

    @Override
    public List<ContactResponseDto> getAllContacts() {
        return contactRepository.findAll()
                .stream()
                .map(contactMapper::toDto)
                .toList();
    }

    @Override
    public ContactResponseDto getContact(Long id) {
        Contact contact = contactRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Contact not found"));
        return contactMapper.toDto(contact);
    }

    @Override
    public List<ContactGroupByDateDto> getContactsGroupedByDate() {
        List<Contact> contacts = contactRepository.findAllByOrderByCreatedAtDesc();

        Map<LocalDate, List<Contact>> grouped =
                contacts.stream()
                        .filter(c -> c.getCreatedAt() != null)
                        .collect(Collectors.groupingBy(
                                contact -> contact.getCreatedAt().toLocalDate(),
                                LinkedHashMap::new,
                                Collectors.toList()
                        ));

        return grouped.entrySet()
                .stream()
                .map(entry ->
                        new ContactGroupByDateDto(
                                entry.getKey(),
                                entry.getValue()
                        )
                )
                .toList();
    }

    @Override
    public ContactResponseDto updateContact(Long id, UpdateContactStatusRequestDto dto) {
        Contact contact = contactRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Contact not found"));

        contact.setStatus(dto.getStatus());
        return contactMapper.toDto(contactRepository.save(contact));
    }

    @Override
    public int getCountContactStatus(int status) {
        return contactRepository.countContactByStatus(status);
    }

    @Override
    public int updateAllContactsStatus() {
        return contactRepository.updateAllStatus0To1();
    }

    @Override
    public void deleteContact(Long id) {
        Contact contact = contactRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Contact not found"));

        contactRepository.delete(contact);
    }
}
