

class UiElement(object):
    def __init__(self, driver):
        self.driver = driver


class Auth0LoginElements(UiElement):
    @property
    def login_green_button(self):
        return self.driver.find_element_by_css_selector(".Login__button")

    @property
    def auth0_lock_button(self):
        return self.driver.find_element_by_css_selector(".auth0-lock-social-button")

    @property
    def not_your_account_button(self):
        return self.driver.find_element_by_css_selector(".auth0-lock-alternative-link")

    @property
    def username_input(self):
        return self.driver.find_element_by_css_selector(".auth0-lock-input[name = username]")

    @property
    def password_input(self):
        return self.driver.find_element_by_css_selector(".auth0-lock-input[name = password]")

    @property
    def login_grey_button(self):
        return self.driver.find_element_by_css_selector(".auth0-lock-submit")


class GuideElements(UiElement):
    @property
    def got_it_button(self):
        return self.driver.find_element_by_css_selector(".button--green")

    @property
    def guide_button(self):
        return self.driver.find_element_by_css_selector(".Helper-guide-slider")

    @property
    def helper_button(self):
        return self.driver.find_element_by_css_selector(".Helper__button--open")


class AddProjectElements(UiElement):
    @property
    def create_new_button(self):
        return self.driver.find_element_by_css_selector(".btn--import")

    @property
    def project_title_input(self):
        return self.driver.find_element_by_css_selector(".CreateLabbook input")

    @property
    def project_description_input(self):
        return self.driver.find_element_by_css_selector(".CreateLabbook__description-input")

    @property
    def project_continue_button(self):
        return self.driver.find_element_by_xpath("//button[contains(text(), 'Continue')]")


class AddProjectBaseElements(UiElement):
    @property
    def arrow_button(self):
        return self.driver.find_element_by_css_selector(".slick-arrow slick-next")

    @property
    def create_project_button(self):
        return self.driver.find_element_by_css_selector(".ButtonLoader ")

    @property
    def projects_page_button(self):
        return self.driver.find_element_by_css_selector(".SideBar__icon")

    @property
    def py2_minimal_base_button(self):
        return self.driver.find_element_by_css_selector("h6[data-name='python2-minimal']")

    @property
    def py3_minimal_base_button(self):
        return self.driver.find_element_by_css_selector("h6[data-name='python3-minimal']")

    @property
    def py3_data_science_base_button(self):
        return self.driver.find_element_by_css_selector("h6[data-name='python3-data-science']")

    @property
    def r_tidyverse_base_button(self):
        return self.driver.find_element_by_css_selector("h6[data-name='r-tidyverse']")


class EnvironmentElements(UiElement):
    @property
    def environment_tab_button(self):
        return self.driver.find_element_by_css_selector("#environment")

    @property
    def add_packages_button(self):
        return self.driver.find_element_by_css_selector(".PackageDependencies__addPackage")

    @property
    def package_name_input(self):
        return self.driver.find_element_by_css_selector(".PackageDependencies__input")

    @property
    def version_name_input(self):
        return self.driver.find_element_by_css_selector(".PackageDependencies__input--version")

    @property
    def add_button(self):
        return self.driver.find_element_by_css_selector(".PackageDependencies__btn--round")

    @property
    def install_packages_button(self):
        return self.driver.find_element_by_css_selector(".PackageDependencies__btn--absolute")

    @property
    def pip_tab_button(self):
        return self.driver.find_element_by_css_selector(".PackageDependencies__btn--absolute")

    @property
    def apt_tab_button(self):
        return self.driver.find_element_by_css_selector(".PackageDependencies__tab:nth-child(3)")

    @property
    def conda3_tab_button(self):
        return self.driver.find_element_by_css_selector(".PackageDependencies__tab:nth-child(2)")

    @property
    def custom_docker_edit_button(self):
        return self.driver.find_element_by_css_selector(".CustomDockerfile__edit-button")

    @property
    def custom_docker_text_input(self):
        return self.driver.find_element_by_css_selector(".CustomDockerfile__textarea")

    @property
    def custom_docker_save_button(self):
        return self.driver.find_element_by_css_selector(".CustomDockerfile__content-save-button")


class ContainerStatus(UiElement):
    @property
    def container_status_stop(self):
        return self.driver.find_element_by_css_selector(".flex>.Stopped")


class ImportProjectElements(UiElement):
    @property
    def import_existing_button(self):
        return self.driver.find_element_by_css_selector(".btn--import~.btn--import")

    @property
    def project_url_input(self):
        return self.driver.find_element_by_css_selector(".Import__input")

    @property
    def import_button(self):
        return self.driver.find_element_by_css_selector("button~button")


class SideBarElements(UiElement):
    @property
    def projects_icon(self):
        return self.driver.find_element_by_css_selector(".SideBar__nav-item--labbooks")

    @property
    def username_button(self):
        return self.driver.find_element_by_css_selector("#username")

    @property
    def logout_button(self):
        return self.driver.find_element_by_css_selector("#logout")


class AddDatasetElements(UiElement):
    @property
    def dataset_page_tab(self):
        return self.driver.find_element_by_xpath("//a[contains(text(), 'Datasets')]")

    @property
    def create_new_button(self):
        return self.driver.find_element_by_css_selector(".btn--import")

    @property
    def dataset_title_input(self):
        return self.driver.find_element_by_css_selector(".CreateLabbook input")

    @property
    def dataset_description_input(self):
        return self.driver.find_element_by_css_selector(".CreateLabbook__description-input")

    @property
    def dataset_continue_button(self):
        return self.driver.find_element_by_xpath("//button[contains(text(), 'Continue')]")

    @property
    def gigantum_cloud_button(self):
        return self.driver.find_element_by_xpath("//h6[contains(text(), 'Gigantum Cloud')]")

    @property
    def create_dataset_button(self):
        return self.driver.find_element_by_css_selector(".ButtonLoader")

    @property
    def publish_dataset_button(self):
        return self.driver.find_element_by_css_selector(".BranchMenu__btn--sync--publish")

    @property
    def dataset_cloud_page(self):
        return self.driver.find_element_by_css_selector(".Datasets__nav-item--cloud")

    @property
    def publish_confirm_button(self):
        return self.driver.find_element_by_css_selector(".VisibilityModal__buttons>button")


class BranchElements(UiElement):
    @property
    def create_branch_button(self):
        return self.driver.find_element_by_css_selector(".Btn--branch--create")

    @property
    def branch_name_input(self):
        return self.driver.find_element_by_css_selector("#CreateBranchName")

    @property
    def create_button(self):
        return self.driver.find_element_by_css_selector(".CreateBranch__buttons .ButtonLoader")

    @property
    def manage_branches_button(self):
        return self.driver.find_element_by_css_selector(".Btn--branch--manage")


class PublishProjectElements(UiElement):
    @property
    def publish_project_button(self):
        return self.driver.find_element_by_css_selector(".Btn--branch--sync--publish")

    @property
    def publish_confirm_button(self):
        return self.driver.find_element_by_css_selector(".VisibilityModal__buttons .Btn--last")

    @property
    def project_page_tab(self):
        return self.driver.find_element_by_css_selector(".SideBar__nav-item--labbooks")

    @property
    def cloud_tab(self):
        return self.driver.find_element_by_css_selector(".Labbooks__nav-item--cloud")

    @property
    def local_tab(self):
        return self.driver.find_element_by_css_selector(".Labbooks__nav-item--local")

    @property
    def sync_project_button(self):
        return self.driver.find_element_by_css_selector(".BranchMenu__btn--sync--upToDate")

    @property
    def delete_project_button(self):
        return self.driver.find_element_by_css_selector(".RemoteLabbooks__icon--delete")

    @property
    def delete_project_input(self):
        return self.driver.find_element_by_css_selector("#deleteInput")

    @property
    def delete_confirm_button(self):
        return self.driver.find_element_by_css_selector(".ButtonLoader")

    @property
    def publish_continue_button(self):
        return self.driver.find_element_by_xpath("//button[contains(text(), 'Continue')]")

    @property
    def publish_private_project_button(self):
        return self.driver.find_element_by_xpath("//label[@for='project_private']")

    @property
    def publish_private_dataset_button(self):
        return self.driver.find_element_by_xpath("//label[@class='PublishDatasetsModal__private-label']")

    @property
    def publish_all_button(self):
        return self.driver.find_element_by_xpath("//button[contains(text(), 'Publish All')]")

    @property
    def collaborators_button(self):
        return self.driver.find_element_by_css_selector(".Collaborators__btn")

    @property
    def select_permission_button(self):
        return self.driver.find_element_by_css_selector(".CollaboratorsModal__permissions")

    @property
    def select_admin_button(self):
        return self.driver.find_element_by_xpath("//div[contains(text(), 'Admin')]")

    @property
    def collaborators_input(self):
        return self.driver.find_element_by_css_selector(".CollaboratorsModal__input--collaborators")

    @property
    def add_collaborators_button(self):
        return self.driver.find_element_by_css_selector(".CollaboratorsModal__btn--add")

    @property
    def close_collaborators_button(self):
        return self.driver.find_element_by_css_selector(".Modal__close")

    @property
    def import_first_cloud_project_button(self):
        return self.driver.find_element_by_css_selector(".RemoteLabbooks__icon--cloud-download")


class InputDataElements(UiElement):
    @property
    def input_data_tab(self):
        return self.driver.find_element_by_css_selector("#inputData")



