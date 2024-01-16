<template>
    <div id="footer">
        <a>Created by: Rafał Mironko, Tomasz Smoleń, Martyna Orzechowska, Marcin Polewski, Katia Anikevich</a>
    </div>
</template>
<script>
export default
{

}
</script>
<style scoped lang="scss">
@import '../style/style.scss';
    #footer
    {
        width: 100%;
        height: 100px;
        border-top: 1px solid $border-color2;
        display: flex;
        justify-content: center;
        align-items: center;

        a
        {
            color: $main-color2;
            text-align: center;
        }
    }
</style>