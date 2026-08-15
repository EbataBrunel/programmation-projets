package eajc.group.apv.mapper;

import eajc.group.apv.dto.ContactRequestDto;
import eajc.group.apv.dto.ContactResponseDto;
import eajc.group.apv.entity.Contact;
import org.springframework.stereotype.Component;

@Component
public class ContactMapper {
    public Contact toEntity(ContactRequestDto dto){
        Contact contact = new Contact();
        contact.setLastName(dto.getLastName());
        contact.setFirstName(dto.getFirstName());
        contact.setEmail(dto.getEmail());
        contact.setPhone(dto.getPhone());
        contact.setMessage(dto.getMessage());
        contact.setStatus(0);
        return contact;
    }

    public ContactResponseDto toDto(Contact contact){
        ContactResponseDto dto = new ContactResponseDto();
        dto.setPublicId(contact.getPublicId());
        dto.setLastName(contact.getLastName());
        dto.setFirstName(contact.getFirstName());
        dto.setEmail(contact.getEmail());
        dto.setPhone(contact.getPhone());
        dto.setMessage(contact.getMessage());
        dto.setStatus(contact.getStatus());
        dto.setCreatedAt(contact.getCreatedAt());
        return dto;
    }
}
