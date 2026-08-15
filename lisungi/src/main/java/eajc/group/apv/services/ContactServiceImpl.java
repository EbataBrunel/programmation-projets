package eajc.group.apv.services;

import eajc.group.apv.dto.*;
import eajc.group.apv.entity.Contact;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.ContactMapper;
import eajc.group.apv.repository.ContactRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@Transactional
public class ContactServiceImpl implements ContactService{

    private final ContactRepository contactRepository;
    private final ContactMapper contactMapper;

    public ContactServiceImpl(ContactRepository contactRepository, ContactMapper contactMapper) {
        this.contactRepository = contactRepository;
        this.contactMapper = contactMapper;
    }

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
    public ContactResponseDto getContact(UUID publicId) {
        Contact contact = contactRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Contact not found"));
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
    public ContactResponseDto updateContact(UUID publicId, UpdateContactStatusRequestDto dto) {
        Contact contact = contactRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Contact not found"));

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
    public void deleteContact(UUID publicId) {
        Contact contact = contactRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Contact not found"));

        contactRepository.delete(contact);
    }
}
